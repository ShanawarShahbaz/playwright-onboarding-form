# AI PR Review Agent

The GitHub Actions workflow in `.github/workflows/pr-review.yml` adds one
advisory AI code review comment to every ready, same-repository pull request.
On subsequent commits, it updates that comment instead of creating noise.

## What it reviews

The agent receives the pull request diff only (up to 100,000 characters). It
looks for evidence-based issues involving correctness, security, regressions,
accessibility, test coverage, and maintainability. It does not run PR code,
approve or merge pull requests, or replace the end-to-end QA workflow.

## Enable it

1. In GitHub, open the repository's **Settings → Secrets and variables →
   Actions**.
2. Add a repository secret named `OPENAI_API_KEY` with an API key from the
   OpenAI Platform. Never put the key in this repository or in a workflow file.
3. Push the workflow to `main` and open a non-draft pull request from a branch
   in this repository.

The job is intentionally skipped for forked pull requests. It uses GitHub's
trusted-base-branch pull-request event but never checks out or executes PR
code, so a changed workflow in the PR cannot access the API secret. Review fork
PRs manually, or use a separate approval-gated workflow if you later need that
capability.

The workflow uses the Responses API with `store: false`, a 1,500-output-token
limit, and the configurable `OPENAI_MODEL` workflow environment variable.
`gpt-5.4-mini` is the default for this bounded code-review task; change the
environment value if you want a different quality/cost trade-off.
