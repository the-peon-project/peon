# PEON Orchestrator Guide

This directory owns the core PEON orchestration API. It is the control plane that other services in this repo depend on. Formerly the standalone `peon-orc` repo, now `peon/services/orc/` in the consolidated `peon` monorepo (see the root `CLAUDE.md` for the overall map).

## Scope

- API entrypoint: `app/main.py`
- API resources: `app/modules/api_v1.py`
- Server lifecycle logic: `app/modules/servers.py`
- Scheduler logic: `app/modules/scheduler.py`
- Plan ingestion and updates: `app/modules/plans.py`, `app/modules/github.py`
- Automated tests: `tests/`

## Runtime Map

- Language/runtime: Python + FastAPI + uvicorn (see `requirements.txt` — this repo's stack has moved on from Flask/Flask-RESTful since that framing was written)
- Main port: `5000`
- Main startup: `python3 app/main.py`
- Dependencies are defined in `requirements.txt`

## Working Rules

1. Start from the API resource or module that actually computes the behavior, not just the route registration.
2. Keep authorization checks intact when changing endpoints.
3. Treat Docker, filesystem, and scheduler interactions as operationally sensitive; prefer non-destructive validation.
4. If endpoint payloads change, review likely consumers in `peon/services/webui/`, `peon/services/bot-discord/`, and `peon/cli/`.
5. If server-management semantics change, update `peon/docs/` source docs.

## Commands

```bash
cd /home/richard/development/peon/services/orc
python3 -m pip install -r requirements.txt
python3 app/main.py
```

## Safe Validation

```bash
cd /home/richard/development/peon/services/orc
python3 -m py_compile app/main.py
```

Use targeted syntax checks or module-level verification around touched files when possible. A pytest suite exists at `tests/` covering the `/api/v1/plans` and `/api/v1/server` routes — run it with `python3 -m pip install -r requirements-dev.txt && python3 -m pytest tests` before considering an API-layer change validated. If the host's system Python is externally managed (PEP 668, `error: externally-managed-environment`), use a local venv instead: `python3 -m venv .venv && .venv/bin/python -m pip install -r requirements-dev.txt && .venv/bin/python -m pytest tests` (`.venv/` is gitignored).

## Important Files

- Startup: `app/main.py`
- API resources: `app/modules/api_v1.py`
- Shared helpers: `app/modules/shared.py`
- Security checks: `app/modules/security.py`
- Server operations: `app/modules/servers.py`
- Scheduler: `app/modules/scheduler.py`
- Plans integration: `app/modules/plans.py`, `app/modules/github.py`
- Repo dependencies: `requirements.txt`
- Test suite: `tests/` (dev dependencies in `requirements-dev.txt`)

## Warplan Source

- Game plan definitions live at `peon/warplans/` in this same repo.
- `config/docker-compose/02_orc.yml` bind-mounts `warplans/` read-only directly into the orc container at `/home/peon/plans` — this repo is always checked out as a full monorepo wherever `deploy_peon.sh` runs (it reads `./config/docker-compose/*.yml` via a relative path), so the plans are always already on disk and always current with no separate fetch step.
- `app/modules/github.py`'s `get_plans_from_github`/`update_plans_from_github` are now no-ops kept only so `PUT /api/v1/plans` (called by webui/bot-discord's "refresh plans" actions) still returns `{"status": "success"}` — refreshing plans now means updating the host's `warplans/` checkout (e.g. `git pull`) rather than triggering an in-container fetch.
- `services/webui/backend/routes/proxy.py`'s `GET /proxy/plans` also reads `warplans/` directly (mounted at `/app/warplans` via `config/docker-compose/03_webui.yml`) — previously this mount didn't exist and the endpoint silently returned an empty list.
- Known pre-existing duplication (not fixed by this change): `app/bin/` contains committed copies of the same scripts that live in `peon/cli/bin/`. Worth deduping at some point but out of scope for this pass.

## Cross-Directory Dependencies (within this repo)

- `peon/services/webui` depends on this API for orchestrator and server control
- `peon/services/bot-discord` depends on this API for Discord command behavior
- `peon/cli` often mirrors operational actions against the PEON stack
- `peon/warplans` defines the recipes this directory consumes
- `peon/wartable` defines the runtime images referenced by plans

## Deployment / Release Validation

**The docker compose flow is the only sanctioned way to build and ship a feature** — running `python3 app/main.py` locally is for iteration only and never counts as shipped. For deployment or release validation, build updated images from source under this directory, then upgrade the UAT/prod stack at `/home/richard/peon/` (a separate deployed instance, distinct from this dev checkout — reachable at `https://server.warcamp.org`) via `peon/deploy_peon.sh` before sign-off. Do not treat local-only startup as final release validation when deployment outcomes are part of the task.

## Safety Notes

- Avoid broad live-container operations as a first validation step.
- Changes to create, destroy, update, or scheduler flows can mutate real server state.
- Prefer syntax checks, focused reads, and clearly scoped local validation before any runtime action.

## Default Workflow

1. Find the owning module under `app/modules/`.
2. Read the endpoint and the underlying helper that mutates state.
3. Make the smallest change that fixes the root cause.
4. Run a narrow syntax or startup validation.
5. Check whether downstream consumers (`peon/services/webui`, `peon/services/bot-discord`, `peon/cli`) or `peon/docs/` need updates.
