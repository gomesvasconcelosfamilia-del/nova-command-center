# NOVA Command Center — public website

This is the **public presentation site only**. Internal engineering dashboards and private repositories remain separate.

## Deployment

The root `index.html` is the only approved public asset.

1. Review PR and merge manually after security review.
2. In repository **Settings → Pages → Build and deployment**, select **GitHub Actions**.
3. The workflow publishes the root HTML only on changes to `main` or manual dispatch.
4. Verify the deployed URL and inspect the page source for private information.

Expected URL after Pages is enabled and a deployment succeeds:
`https://gomesvasconcelosfamilia-del.github.io/nova-command-center/`

**Not yet live** until Pages is enabled and a deployment succeeds.

## Safety

- No repository/PR inventory, internal project status, tokens, authentication or private APIs in this site.
- Workflow stages only the approved `index.html`, never the entire repository.
- No NOVA Operator integration.
- No automatic merges or releases.
- No claims of tested binaries, build success, or product availability.

## Future improvements

A real private Command Center should use authentication and a backend or trusted GitHub Actions-produced **sanitized** data feed. Do not put a private GitHub token in browser JavaScript.
