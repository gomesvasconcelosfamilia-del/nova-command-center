# NOVA — private admin foundation (not deployed)

The public GitHub Pages site **cannot** secure an administrator dashboard by hiding HTML, adding a login button, or storing a GitHub token in JavaScript. The private administration API must run on a separate authenticated origin.

## Recommended architecture

1. Public: GitHub Pages at the existing URL; no private data or login tokens.
2. Private: Cloudflare Worker behind a **Cloudflare Access application** covering the entire Worker hostname/path.
3. Authentication: Access policy restricted to the owner's identity; use an identity provider with passkey/WebAuthn or device biometric authentication. **Cloudflare Access alone does not automatically guarantee a biometric factor.** Enforce the required authentication strength at the identity provider.
4. Authorization: the Worker also verifies the signed Access JWT (RS256, issuer, audience, expiry and administrator email).
5. GitHub: use a fine-grained GitHub token with **read-only metadata access to explicitly selected repositories**, stored as a Worker secret. Prefer a narrowly scoped GitHub App later. No write/merge API in this version.
6. Private UI: serve from a separately protected hostname and only call same-origin API endpoints. Never embed private data in GitHub Pages.

## Configuration required before deployment

Cloudflare account and domain/hostname; Access team domain (e.g. `https://example.cloudflareaccess.com`), application AUD tag, owner email, approved repository allowlist, GitHub token. These values **must not be committed**.

Worker environment:
- `ACCESS_TEAM_DOMAIN` — exact https team domain
- `ACCESS_AUD` — Access application audience tag
- `ADMIN_EMAIL` — exact approved email
- `GITHUB_REPOS` — comma-separated `gomesvasconcelosfamilia-del/repo` allowlist
- `GITHUB_TOKEN` — **secret**, never plaintext in config/repo

## Routes (authenticated only)
- `GET /api/health` — private API health; not public health.
- `GET /api/repos` — limited metadata from allowlisted GitHub repositories.
- All other routes return 404; all non-GET methods return 405.

## Before go-live

- Configure Access **before** pointing any private hostname at the Worker; deny all by default.
- Set up passkeys/WebAuthn in the identity provider; test biometric entry on Xiaomi and Mac.
- Configure Worker secrets outside GitHub.
- Test invalid/expired/forged JWT, incorrect audience, incorrect email, missing token, and unapproved repo.
- Check Worker hostname is not reachable without Access; test directly and through custom domain.
- Review GitHub token repository permissions and rotate it if exposed.
- Enable audit logs and a recovery login method in case biometrics are unavailable.
- Consider Cloudflare plan limits and pricing before enabling; no claim of zero-cost availability is made here.

**No Worker, Access application, secrets, domain, GitHub token or private dashboard has been deployed or created.** This is source code and a deployment/security plan only.
