# NOVA Command Center — publication and privacy checks

These are lightweight source-level checks for the public page. They do **not** replace browser testing, a security review, or a successful GitHub Pages deployment.

## Verified from source
- Language is `pt-PT`.
- Navigation links have matching section IDs.
- No JavaScript is embedded in the public page.
- No internal GitHub repository URLs are embedded.
- No GitHub personal-access-token-like strings are embedded.

## Still to verify
- GitHub Pages is enabled and the deployment workflow completes successfully.
- Mobile and desktop visual smoke tests.
- Accessibility with keyboard and screen reader.
- Privacy review before adding any new content, analytics or external integrations.

The public website must remain separate from the private engineering command dashboard. Do not publish private PRs, repository inventories, CI logs, licensing secrets or customer data.
