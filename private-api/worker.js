// NOVA private admin API — Cloudflare Worker (not deployed).
// Requires Cloudflare Access in front of this Worker, plus independent JWT verification here.
const json=(data,status=200)=>new Response(JSON.stringify(data),{status,headers:{"content-type":"application/json; charset=utf-8","cache-control":"no-store","x-content-type-options":"nosniff"}});
const decode=s=>{const b=s.replace(/-/g,"+").replace(/_/g,"/");return Uint8Array.from(atob(b.padEnd(Math.ceil(b.length/4)*4,"=")),c=>c.charCodeAt(0))};
const parse=s=>JSON.parse(new TextDecoder().decode(decode(s)));
async function accessIdentity(request,env){
  const token=request.headers.get("cf-access-jwt-assertion");
  if(!token||token.length>12000)throw Error("missing assertion");
  const parts=token.split(".");if(parts.length!==3)throw Error("invalid assertion");
  const header=parse(parts[0]),claims=parse(parts[1]);
  if(header.alg!=="RS256"||typeof header.kid!=="string")throw Error("unexpected algorithm");
  const domain=env.ACCESS_TEAM_DOMAIN;
  if(!/^https:\/\/[a-z0-9-]+\.cloudflareaccess\.com$/.test(domain||""))throw Error("invalid Access configuration");
  const jwksResponse=await fetch(domain+"/cdn-cgi/access/certs",{cf:{cacheTtl:300,cacheEverything:true}});
  if(!jwksResponse.ok)throw Error("Access key lookup failed");
  const jwks=await jwksResponse.json();
  const jwk=jwks.keys?.find(k=>k.kid===header.kid&&k.kty==="RSA"&&(!k.alg||k.alg==="RS256")&&(!k.use||k.use==="sig"));
  if(!jwk)throw Error("unknown signing key");
  const key=await crypto.subtle.importKey("jwk",jwk,{name:"RSASSA-PKCS1-v1_5",hash:"SHA-256"},false,["verify"]);
  const valid=await crypto.subtle.verify("RSASSA-PKCS1-v1_5",key,decode(parts[2]),new TextEncoder().encode(parts[0]+"."+parts[1]));
  const now=Math.floor(Date.now()/1000);
  if(!valid||claims.iss!==domain||!Array.isArray(claims.aud)||!claims.aud.includes(env.ACCESS_AUD)||typeof claims.exp!=="number"||claims.exp<=now||typeof claims.iat!=="number"||claims.iat>now+60||(claims.nbf!==undefined&&claims.nbf>now))throw Error("invalid claims");
  if(typeof claims.email!=="string"||claims.email.toLowerCase()!==env.ADMIN_EMAIL?.toLowerCase())throw Error("not administrator");
  return claims.email;
}
export default {
 async fetch(request,env){
  if(request.method!=="GET")return json({error:"method_not_allowed"},405);
  const path=new URL(request.url).pathname;
  if(path!=="/api/health"&&path!=="/api/repos")return json({error:"not_found"},404);
  try{await accessIdentity(request,env)}catch{return json({error:"unauthorized"},401)}
  if(path==="/api/health")return json({ok:true,mode:"private-read-only"});
  if(!env.GITHUB_TOKEN||!env.GITHUB_REPOS)return json({error:"server_not_configured"},503);
  const repos=env.GITHUB_REPOS.split(",").map(s=>s.trim()).filter(Boolean);
  if(repos.length===0||repos.length>30||repos.some(s=>!/^gomesvasconcelosfamilia-del\/[A-Za-z0-9_.-]+$/.test(s)))return json({error:"invalid_allowlist"},503);
  const results=await Promise.all(repos.map(async name=>{
   try{
    const res=await fetch("https://api.github.com/repos/"+name,{headers:{"Authorization":"Bearer "+env.GITHUB_TOKEN,"Accept":"application/vnd.github+json","User-Agent":"nova-command-center-private-api","X-GitHub-Api-Version":"2022-11-28"}});
    if(!res.ok)return {name,error:"github_unavailable",status:res.status};
    const x=await res.json();return {name:x.full_name,private:x.private,default_branch:x.default_branch,open_issues_count:x.open_issues_count,updated_at:x.updated_at};
   }catch{return {name,error:"github_unavailable"}}
  }));
  return json({repos:results,read_only:true});
 }
};
