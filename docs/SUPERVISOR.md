# NOVA automated supervisor — phase 1

Daily at 08:41 UTC, and on manual dispatch, a GitHub Actions workflow reads **only this public repository** and generates a JSON report and Markdown summary containing open PRs, draft flags, inactivity age and recent workflow failures. Reports are stored as GitHub Actions artifacts, **not** on the public website.

- No external credentials, private repositories or write operations.
- No automatic merges or issue creation.
- Does not claim to coordinate real agents or verify plugin builds.
- This workflow is the first public-safe reporting step. A private cross-repository supervisor must be implemented in a **private** repository with explicitly scoped GitHub App credentials and private artifact storage.
- GitHub Actions schedules may run late or be skipped; reports are best-effort.
- Artifact access follows GitHub's repository visibility. Never include sensitive information in artifacts of a public repository.

Next: separate private GitHub Issues/Projects task board, scoped Actions check runners, authenticated private dashboard and safe merge gates.
