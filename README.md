# Prismatic Deploy Pilot

Minimal service proving Prismatic's multi-repo post-merge deploy pipeline
works for a repo that is not `prismatic-engine`.

- `GET /health` → `{"ok": true, "version": "<version>"}`
- `GET /version` → plain-text version

Deploys are driven by `.github/workflows/post-merge-deploy.yml`, which POSTs
an HMAC-signed trigger to the Prismatic deploy receiver on merge to `main`.
The receiver builds a wheel, installs it into a fresh venv, flips the
per-repo release symlinks, restarts `prismatic-deploy-pilot.service`, and
health-checks — rolling back automatically on failure.
