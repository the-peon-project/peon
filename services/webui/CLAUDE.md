# PEON Web UI Guide

This directory owns the PEON dashboard application. It is the busiest application surface in the monorepo and the only directory with a clear committed automated test suite. Formerly the standalone `peon-webui` repo, now `peon/services/webui/` in the consolidated `peon` monorepo (see the root `CLAUDE.md` for the overall map).

## Scope

- Backend API: `backend/`
- Frontend app: `frontend/`
- Python tests: `tests/`
- Docker packaging: `Dockerfile`, `docker-compose.example.yml`
- Only 329 files are tracked in git under this directory; `frontend/node_modules` (493M) is gitignored and not part of the repo.

## Runtime Map

- Backend framework: FastAPI
- Backend entrypoint: `backend/server.py`
- Backend default port: `8001`
- Frontend stack: React + CRACO
- Frontend entrypoint: `frontend/src/App.js`
- Frontend default port: `3000`
- Persistent backend data: SQLite under `/data` in containerized runs

## Working Rules

1. Treat backend and frontend as separate validation surfaces.
2. When changing API shapes, check frontend consumers in `frontend/src/` and backend route definitions in `backend/routes/`.
3. When changing auth, permissions, or admin flows, inspect tests under `tests/` before editing.
4. Keep Docker and local-development commands aligned when ports, env vars, or startup behavior change.
5. Keep changes minimal and directory-local unless the task is explicitly cross-directory; prefer non-destructive validation first.
6. If user-visible behavior changes, update `peon/docs` source docs in the same pass.
7. Do not request or print secrets, and do not hand-edit generated docs outputs directly.
8. For deployment or release validation, build updated images from source under this directory, then upgrade the UAT stack at `/home/richard/peon/` (a separate deployed instance, distinct from this dev checkout — reachable at `https://server.warcamp.org`) via `peon/deploy_peon.sh` before sign-off.

## Commands

### Backend

```bash
cd /home/richard/development/peon/services/webui/backend
python3 -m pip install -r requirements.txt
python3 server.py
```

### Frontend

```bash
cd /home/richard/development/peon/services/webui/frontend
yarn install
yarn start
```

### Tests

```bash
cd /home/richard/development/peon/services/webui
python3 -m pytest tests

cd /home/richard/development/peon/services/webui/frontend
CI=true yarn test --watchAll=false
```

## Important Files

- Backend app: `backend/server.py`
- Backend config: `backend/core/config.py`
- Backend routes: `backend/routes/`
- Frontend package metadata: `frontend/package.json`
- Frontend app root: `frontend/src/App.js`
- API tests: `tests/test_peon_dashboard.py`
- Permission tests: `tests/test_role_permissions.py`
- Docker example: `docker-compose.example.yml`

## Validation Expectations

- Backend route or auth changes: run `python3 -m pytest tests`, where practical.
- Frontend UI logic changes: run focused CRACO/Jest checks via `CI=true yarn test --watchAll=false`.
- Broad full-stack changes: validate backend tests first, then frontend tests.
- If tests rely on external environment configuration, say so explicitly in the result.

## Known Constraints

- The committed Python tests use HTTP requests and may rely on a configured backend target via `REACT_APP_BACKEND_URL`.
- Frontend scripts are CRACO-based: `start`, `build`, and `test` are all routed through CRACO.
- Backend CORS, secrets, and sync interval are configured in `backend/core/config.py` and `.env`.

## Cross-Directory Dependencies (within this repo)

- Calls `peon/services/orc` APIs for orchestrator and server control.
- User-visible behavior should be reflected in `peon/docs`.
- Backend assumptions about plans or images may require checking `peon/warplans` or `peon/wartable`.
- Bot-facing behavior parity may involve `peon/services/bot-discord` if it surfaces the same orchestrator actions.
- Deployment/composition wiring for this service lives at the repo root (`peon/config/docker-compose/`, `peon/deploy_peon.sh`).

## Default Workflow

1. Identify whether the change is backend, frontend, or both.
2. Read the owning route/component/test first.
3. Make the smallest directory-local edit.
4. Run the narrowest backend or frontend validation that can fail meaningfully.
5. Check whether `peon/docs` also needs to change.
