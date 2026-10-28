# Docker & Container Security — FestPass

## Student Details

- Name: Anushka Singh
- REGNO: 8074
- PORT: 8074
- Docker Hub username: `anushkaa02`
- Docker Hub repository: https://hub.docker.com/r/anushkaa02/fest-backend

## Project Overview

This repository contains a Flask/PostgreSQL backend and an Nginx-served FestPass registration frontend for the five-stage Docker and container security assessment. Registrations are stored in PostgreSQL and can be listed after service restarts.

The Dockerfile contains a `stage1` target using `python:3.9` and a `fixed` target using the pinned `python:3.14.10-slim-trixie` image with a non-root runtime user. `compose.stage2.yaml` temporarily selects the local Stage 1 backend; final `compose.yaml` references the published `1.0.0` image.

## Architecture

The browser loads the static frontend from Nginx on host port 8074. Nginx proxies `/health` and `/api/*` to the Flask backend on port 5000. The backend communicates with PostgreSQL at `db`; PostgreSQL persists data in the named `postgres_data` volume. The frontend/backend network is separate from the backend/database network.

## AI Tools Used

- GitHub Copilot: prepared Docker and Compose configuration, assessment documentation, and configuration consistency checks.
- ChatGPT: not used for these repository changes; GitHub Copilot was used for the configuration and documentation preparation.

## Stage Checklist

- [x] Stage 1: build, run, and verify `fest-backend:0.1` (execution passed; screenshots pending).
- [ ] Stage 2: start frontend, backend, and PostgreSQL; verify health and persistence.
- [x] Stage 3: build and scan `fest-backend:0.2`; reports saved (evidence screenshots pending).
- [ ] Stage 4: push both release tags and record the real immutable digest.
- [ ] Stage 5: generate the Cosign key pair, sign and verify `1.0.0`, and confirm unsigned `1.0.1` is rejected.

No stage is complete until its commands have been run and actual results checked.

## Security Results

| Image | CRITICAL | HIGH | Image size |
| --- | --- | --- | --- |
| Before: `fest-backend:0.1` | 234 | 2,246 | 1.62GB |
| After: `fest-backend:0.2` | 0 | 49 | 209MB |

Reports are stored in `reports/trivy-before.txt` and `reports/trivy-after.txt`. The after-image CRITICAL gate passed; 49 HIGH findings remain and should be reviewed.

## Docker Hub Release

- `APP_VERSION`: `1.0.0`
- Required tags: `anushkaa02/fest-backend:1.0.0` and `anushkaa02/fest-backend:1.0`
- Immutable `1.0.0` digest: TBD
- Local `1.0.0` and `1.0` images built; push attempt failed because the configured Docker Hub token lacks repository scope.

Update the digest only from actual Docker Hub inspection output. `compose.yaml` is prepared to use `anushkaa02/fest-backend:1.0.0`.

## Incomplete Steps and Prerequisites

- Stage 1 and fixed-image builds succeeded. Stage 1 container health returned `{"regno":"8074","status":"ok"}`; the fixed image ran as UID 10001 and returned the same health status. Required terminal screenshots are still pending.
- Compose has not been started because a private `POSTGRES_PASSWORD` must first be set in local `.env`.
- Trivy 0.76.1 was installed in the user-local bin directory and both scans were run. Cosign is not installed; no signature verification has been performed.
- Docker Hub publishing requires an account token with write scope for `anushkaa02/fest-backend`; no digest is available until a push succeeds.
- The unsigned `1.0.1` image is built locally but has not been pushed or verified.
- `.env.example` contains an empty password value. Create `.env` locally and set a private password; `.env` is ignored by Git.
- `cosign.pub` is intentionally absent until you generate the real key pair. Keep the private key local; never add `cosign.key`.
- Trivy reports, Docker Hub digest, signatures, verification output, and screenshots require your real manual execution.

## Evidence

Save required real terminal screenshots in `screenshots/`. Each must show the `[8074]` prompt, command, and actual output.

- `S1-2.png`: immediately after the Stage 1 image build completes.
- `S1-3.png`: after running the Stage 1 container and showing `docker ps` output.
- `S2-2.png`: after Compose starts all three services.
- `S2-3.png`: after showing Compose service status and the PostgreSQL `pg_isready` result.
- `S2-4.png`: after recreating Compose services without deleting the volume and confirming the persistence probe remains.
- `S3-1.png`: after the real before-image Trivy scan.
- `S3-3.png`: after the real fixed-image Trivy scan and CRITICAL gate.
- `S4-1.png`: after showing both local release tags.
- `S4-2.png`: after both Docker Hub pushes succeed.
- `S4-3.png`: after inspecting and recording the actual `1.0.0` digest.
- `S5-1.png`: after key generation; do not reveal private key material.
- `S5-2.png`: after signing by digest and successful verification with `cosign.pub`.
- `S5-3.png`: after building and pushing unsigned `1.0.1`.
- `S5-4.png`: after actual verification output rejects unsigned `1.0.1`.

## Project Structure

```text
8074-docker-assessment/
|-- README.md
|-- compose.yaml
|-- compose.stage2.yaml
|-- .env.example
|-- .gitignore
|-- cosign.pub                 (add your generated public key; not yet present)
|-- backend/
|   |-- app.py
|   |-- requirements.txt
|   |-- Dockerfile
|   `-- .dockerignore
|-- frontend/
|   |-- index.html
|   `-- nginx.conf
|-- reports/
|   |-- trivy-before.txt
|   `-- trivy-after.txt
|-- screenshots/
	|-- .gitkeep
	`-- required evidence files (pending)
```