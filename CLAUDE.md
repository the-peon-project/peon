# PEON Monorepo Guide

This repo is the single source of truth for the PEON project: deployment composition plus every service, tool, and doc source that makes up the stack. It used to be split across 8 repos (`peon`, `peon-orc`, `peon-cli`, `peon-warplans`, `peon-wartable`, `peon-webui`, `peon-bot-discord`, `peon-docs`); all but the generated site have been merged in here via `git subtree` (full commit history preserved per subdirectory — `git log`/`git blame` on any file still shows its pre-merge history). The old standalone repos are deprecated and archived; do not open new work against them.

The one repo that stays separate is `the-peon-project.github.io` — the generated site built from `peon/docs/`, still a sibling directory at the workspace root, not part of this repo.

## Layout

```
peon/
  deploy_peon.sh, docker-compose.yml, config/       deployment composition (this repo's original scope)
  backup/, cache/, certs/, media/, plans/, servers/  runtime/Docker volume dirs (several root-owned)
  services/
    orc/            Python/FastAPI orchestrator API (control plane)          - was peon-orc
    webui/          FastAPI backend + React/CRACO frontend dashboard         - was peon-webui
    bot-discord/    discord.py Discord bot                                   - was peon-bot-discord
  cli/              host-side shell CLI                                     - was peon-cli
  warplans/         game definitions and deployment recipes registry        - was peon-warplans
  wartable/         container image definitions (Steam tooling, base images) - was peon-wartable
  docs/             documentation source (packages into the-peon-project.github.io) - was peon-docs
```

Each subdirectory under `services/`, `cli/`, `warplans/`, `wartable/`, and `docs/` has its own nested `CLAUDE.md` scoped to that area — read the relevant one before working there. This file covers deployment composition (its original scope) plus cross-cutting rules for the whole repo.

## Working Rules

1. Determine the owning subdirectory first — treat each one as its own logical unit even though they now share a git history. Keep changes scoped to it unless the task is explicitly cross-cutting.
2. Read the nested `CLAUDE.md` for the subdirectory you're touching before making changes.
3. For deployment composition specifically: read the compose fragments in `config/docker-compose/` before changing `deploy_peon.sh`.
4. Treat `deploy_peon.sh` as operationally sensitive: it writes `.env`, updates `~/.bashrc`, writes `/etc/motd`, and starts containers. Do not run it as routine validation.
5. If a change affects user-visible or developer-visible behavior, update `docs/manual/docs/` in the same pass.
6. Do not hand-edit `docs/manual/site/` (generated) or `../the-peon-project.github.io/` unless the task explicitly asks for generated-output changes.

## Commands

### Core services

```bash
# Orchestrator
cd /home/richard/development/peon/services/orc
python3 -m pip install -r requirements.txt
python3 app/main.py

# Discord bot
cd /home/richard/development/peon/services/bot-discord
python3 -m pip install -r requirements.txt
python3 app/main.py

# Web UI backend
cd /home/richard/development/peon/services/webui/backend
python3 -m pip install -r requirements.txt
python3 server.py

# Web UI frontend
cd /home/richard/development/peon/services/webui/frontend
yarn install
yarn start
```

### Tests and validation

```bash
# Web UI backend and API tests
cd /home/richard/development/peon/services/webui
python3 -m pytest tests

# Web UI frontend tests
cd /home/richard/development/peon/services/webui/frontend
CI=true yarn test --watchAll=false
```

### Docs packaging

```bash
cd /home/richard/development/peon/docs
./package_docs.sh
```

Only run this when the task includes rebuilding or publishing generated docs — it writes into `/home/richard/development/the-peon-project.github.io/` (an absolute path baked into the script; unaffected by `docs/` now being nested one level deeper than the old standalone `peon-docs` repo was).

## Validation Expectations By Subdirectory

- `services/webui/backend`: run `python3 -m pytest tests` if the change can affect backend behavior.
- `services/webui/frontend`: run frontend tests when UI logic changes; if tests are not targeted enough, at minimum ensure the frontend build or test runner starts cleanly.
- `services/orc`: no committed narrow automated suite; prefer targeted startup and syntax validation around touched files.
- `services/bot-discord`: no committed narrow automated suite; prefer syntax validation and targeted module-level checks.
- `cli`: validate shell changes with targeted script help or specific non-destructive flags.
- `warplans`: validate JSON shape and keep the per-game README aligned with `plan.json` changes.
- `wartable`: validate Docker build surfaces statically; do not push images as a validation step.
- `docs`: validate source markdown and, when requested, rebuild via `./package_docs.sh`.
- Deployment composition (this directory's root files): `bash -n deploy_peon.sh` before considering any operational execution; otherwise prefer static review of compose fragments and environment wiring.

## Important Files

- Deployment composition: `deploy_peon.sh`, `config/docker-compose/`
- Orchestrator config: `config/peon.orchestrators.json`
- Orchestrator API: `services/orc/app/modules/api_v1.py`
- Orchestrator bootstrap: `services/orc/app/main.py`
- CLI entrypoint: `cli/bin/peon`
- Warplan registry: `warplans/plans.json`
- Web UI backend app: `services/webui/backend/server.py`
- Web UI frontend package metadata: `services/webui/frontend/package.json`
- Docs navigation and site config: `docs/manual/zensical.toml`
- Docs publishing script: `docs/package_docs.sh`

## High-Signal Change Patterns

### Adding or changing a game

Usually touches several subdirectories:

1. `warplans/` for the game definition
2. `wartable/` if a container or runtime image changes
3. `services/orc/` if orchestration logic or API assumptions change
4. `docs/` for development and user-facing documentation

### Changing server management behavior

Check impacts across:

1. `services/orc/` for the actual control behavior
2. `services/webui/` if the dashboard depends on the changed endpoint or payload
3. `services/bot-discord/` if bot commands call the same API
4. `cli/` if operator commands mirror the same action

### Changing deployment

Inspect the compose fragments in `config/docker-compose/` before editing `deploy_peon.sh` or any subdirectory's runtime assumptions.

## Cross-Repo Dependencies (within this repo)

- Deployment composition wires together `services/orc`, `services/webui`, `docs`, and `services/bot-discord`
- `services/orc` is the control plane every other service and `cli` calls into
- `services/orc` fetches plans via git: `app/modules/github.py` clones `https://github.com/the-peon-project/peon.git` and sparse-checks-out `warplans/` into a runtime `plans/` directory (`/home/peon/plans` in-container, via `config/docker-compose/02_orc.yml`'s `$PWD/plans:/home/peon/plans` mount) — this is needed because a real deployment host is typically a thin checkout (`deploy_peon.sh` and `config/docker-compose/` only, pulling application code as pre-built images) that does not carry `warplans/` itself. See `services/orc/CLAUDE.md`'s "Warplan Source" section for the full mechanism
- `warplans/` recipes reference `wartable/` images as contract points

## Deployment / Release Validation

**The docker compose flow is the only sanctioned way to build and ship a feature.** A feature is not shipped until it has been built into image(s) and deployed through `deploy_peon.sh` (which composes the fragments in `config/docker-compose/`) to the UAT/prod stack at `/home/richard/peon/`. Running a service natively (`python3 app/main.py`, `yarn start`, etc.), hand-copying files into `/home/richard/peon/`, or standing up containers outside this compose flow is for local iteration only and never counts as shipped.

For any task that includes deployment, release validation, or final runtime verification: build updated service image(s) from source under this dev checkout, then upgrade the UAT stack at `/home/richard/peon/` (a separate deployed instance from this repo, reachable at `https://server.warcamp.org`) to those images via `deploy_peon.sh`, and validate behavior against that upgraded UAT instance. Local unit/syntax checks are useful for iteration, but final sign-off for release-tagged work should be based on the upgraded UAT runtime, not local-only execution. Only take this operational step when explicitly requested.

## Safety Notes

- `deploy_peon.sh` is operational, interactive, and not safe as a routine validation step. It writes `.env`, updates `~/.bashrc`, writes `/etc/motd`, and starts containers.
- Do not request or paste secrets such as Discord tokens or production API keys into chat output.
- Prefer non-destructive validation first.

## Default Workflow

When no more specific instruction exists:

1. Determine the owning subdirectory.
2. Read that subdirectory's nested `CLAUDE.md`.
3. Read only the local files needed to form a concrete hypothesis.
4. Make the smallest grounded edit.
5. Run the narrowest validation available for that subdirectory.
6. Update `docs/` if behavior or developer workflow changed.

Repo-local nested guides:

- `services/orc/CLAUDE.md`
- `services/webui/CLAUDE.md`
- `services/bot-discord/CLAUDE.md`
- `cli/CLAUDE.md`
- `warplans/CLAUDE.md`
- `wartable/CLAUDE.md`
- `docs/CLAUDE.md`

Workspace-wide instructions live in this repo at `AGENTS.md` — the canonical, tool-agnostic source. `CLAUDE.md`, `.github/copilot-instructions.md`, and `QWEN.md` one level up at the workspace root (`/home/richard/development/`) are thin wrappers that point here rather than duplicating its content. Also see `.github/instructions/` and `.claude/commands/` one level up for pattern-specific and slash-command guidance.

## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

Rules:
- For codebase questions, first run `graphify query "<question>"` when graphify-out/graph.json exists. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).
