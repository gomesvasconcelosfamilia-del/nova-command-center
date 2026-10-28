#!/usr/bin/env python3
"""Public repository supervisor: no secrets, no private repository inventory."""
import json
import os
import sys
import urllib.request
from datetime import datetime, timezone

REPO = "gomesvasconcelosfamilia-del/nova-command-center"
API = "https://api.github.com/repos/" + REPO

def get(path):
    req = urllib.request.Request(API + path, headers={
        "Accept": "application/vnd.github+json",
        "User-Agent": "nova-public-supervisor/1",
        "X-GitHub-Api-Version": "2022-11-28",
    })
    with urllib.request.urlopen(req, timeout=20) as response:
        return json.load(response)

def main():
    pulls = get("/pulls?state=open&per_page=100")
    runs = get("/actions/runs?per_page=30").get("workflow_runs", [])
    now = datetime.now(timezone.utc)
    report = {
        "generated_at": now.isoformat(),
        "scope": REPO,
        "visibility": "public-repository-only",
        "open_prs": [],
        "recent_workflows": [],
        "notes": ["No private repositories accessed", "No merge or write actions performed"],
    }
    for p in pulls:
        updated = datetime.fromisoformat(p["updated_at"].replace("Z", "+00:00"))
        days = (now - updated).days
        report["open_prs"].append({
            "number": p["number"],
            "title": p["title"],
            "draft": p["draft"],
            "stale_days": days,
            "needs_attention": days >= 7,
            "url": p["html_url"],
        })
    for run in runs[:20]:
        report["recent_workflows"].append({
            "name": run["name"],
            "status": run["status"],
            "conclusion": run["conclusion"],
            "url": run["html_url"],
        })
    os.makedirs("reports", exist_ok=True)
    with open("reports/supervisor.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    with open("reports/summary.md", "w", encoding="utf-8") as f:
        f.write("# NOVA public repository supervisor\n\n")
        f.write("Generated: " + report["generated_at"] + "\n\n")
        f.write("Open PRs: " + str(len(report["open_prs"])) + "\n\n")
        for p in report["open_prs"]:
            f.write("- #" + str(p["number"]) + " " + p["title"].replace("\n", " ") +
                    (" [DRAFT]" if p["draft"] else "") +
                    (" [STALE]" if p["needs_attention"] else "") + "\n")
        f.write("\n## Recent workflow failures\n")
        for run in report["recent_workflows"]:
            if run["conclusion"] == "failure":
                f.write("- " + run["name"].replace("\n", " ") + ": " + run["url"] + "\n")
    print("Public supervisor completed:", len(pulls), "PRs,", len(report["recent_workflows"]), "workflow runs")
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print("Supervisor failed:", type(e).__name__, str(e), file=sys.stderr)
        sys.exit(1)
