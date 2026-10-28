# NOVA Command Center — GitHub-only architecture

## Product vision
One operational command center across NOVA UNIVERSE, accessible from phone and desktop: projects, tasks, agents, PRs, branches, checks, releases and audited actions. Each agent remains scoped to its assigned project. No cross-plugin changes or global builds.

## Trust boundary
- **Public site:** GitHub Pages, presentation only. Never publish private repository names, issues, PRs, statuses, build logs, internal agent reports, secrets or customer data.
- **Private operations:** GitHub private repositories, Issues, Projects, Actions and authenticated GitHub UI. GitHub authentication and passkeys can protect the **GitHub account**, but do not make GitHub Pages private.
- **Automation:** GitHub Actions with least-privilege `GITHUB_TOKEN` permissions, protected environments, pinned dependencies, explicit repository allowlists, and auditable logs. No browser PAT.
- **Future private web dashboard:** needs a properly authenticated server-side backend or a trusted hosted platform. Not implemented or claimed secure yet.

## Iterative delivery
1. Public dashboard: retain current static presentation and improve navigation and content only.
2. GitHub-only control plane: private Issues/Projects for tasks, Actions for verified checks, PR labels for readiness, branch protection and required checks.
3. Scoped reporting: workflow-generated private artifacts stored in private repositories; never publish to Pages.
4. GitHub-based authenticated management: use GitHub UI as the initial private dashboard; no custom login until server-side auth is available.
5. Agents: opt-in execution with explicit scope and permissions, logs, retries, no unreviewed destructive actions.

## Merge policy
- For **this public presentation repo only**, merge verified, non-sensitive changes after reviewing diff and ensuring no branch protection/check failure.
- For plugin/DSP, release, secret, permission, billing, and infrastructure changes, request explicit approval.
- No merges of draft PRs with unfinished security validation.
- Never mistake an unexecuted check for a passed check.

## Cloudflare
Not required. Prior Cloudflare Worker proof-of-concept is intentionally **not deployed**; keep PR #4 draft and do not merge it into the public-site repository.
