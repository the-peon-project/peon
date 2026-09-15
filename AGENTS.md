# PEON Workspace Guide (generic, tool-agnostic)

This is the canonical, tool-agnostic instructions file for the PEON workspace. It is not specific to any one AI coding assistant — CLAUDE.md, `.github/copilot-instructions.md`, QWEN.md, and any equivalent file for another agentic tool are thin wrappers that point here. Edit this file when workspace facts change; edit a wrapper only to add guidance specific to that tool.

This workspace holds the PEON project. As of the consolidation into a single `peon/` monorepo, only two top-level directories matter:

- `peon/` — this monorepo. Everything (deployment composition, orchestrator, CLI, warplans, wartable, web UI, Discord bot, docs source) lives here now, each in its own subdirectory with full pre-consolidation git history preserved.
- `the-peon-project.github.io/` — the generated site, built from `peon/docs/`. Kept separate deliberately; not part of the monorepo.

The 7 repos this replaced (`peon-orc/`, `peon-cli/`, `peon-warplans/`, `peon-wartable/`, `peon-webui/`, `peon-bot-discord/`, `peon-docs/`) are **deprecated and archived on GitHub**; their content now lives under `peon/` (see the layout below). Only `peon-orc/` still exists on disk at the workspace root — the other 6 have already been removed locally. Where `peon-orc/` is still present, treat it as read-only history and do not start new work in it; if you find yourself about to edit a file under it, stop and make the equivalent edit under `peon/` instead.

## Workspace Scope

- In scope for normal development work: `peon/` (all subdirectories)
- Generated output repo: `the-peon-project.github.io/` — unless a task explicitly asks for generated-site changes, do not edit it directly; its content is built from `peon/docs/`.
- Out of scope / read-only: `peon-orc/` (the only one of the 7 deprecated repos still present on disk; the rest have already been removed locally) — deprecated, archived, superseded by `peon/`

## Project Map

### `peon/`

The monorepo. See `peon/CLAUDE.md` (or your tool's equivalent nested guide) for the full layout diagram and cross-cutting rules. Subdirectories, each with its own nested guide:

- `peon/` root — deployment composition. Entrypoint `deploy_peon.sh`; compose fragments in `config/docker-compose/`.
- `peon/services/orc/` — core orchestrator API (Python + FastAPI). Entrypoint `app/main.py`. Default local port `5000`. The primary control plane other services call.
- `peon/services/webui/` — web dashboard. Backend: FastAPI in `backend/server.py` (port `8001`). Frontend: React + CRACO in `frontend/` (port `3000`). The only subdirectory with an obvious automated test surface committed in-tree.
- `peon/services/bot-discord/` — Discord bot integration (Python + `discord.py`). Entrypoint `app/main.py`.
- `peon/cli/` — host-side shell CLI for managing PEON containers. Entrypoint `bin/peon`, helpers under `bin/modules/`.
- `peon/warplans/` — game definitions and deployment recipes. Registry `plans.json`; per-game structure `<game>/plan.json`, `<game>/README.md`, `<game>/actions/`.
- `peon/wartable/` — container image definitions used by the orchestrator. Focus area `containers/`.
- `peon/docs/` — primary documentation source. Main docs sources `manual/docs/`; site config `manual/zensical.toml`; packaging script `package_docs.sh` (publishes into `../the-peon-project.github.io/` relative to the workspace root, i.e. `/home/richard/development/the-peon-project.github.io` — an absolute path baked into the script, so `docs/` living one level deeper than the old standalone `peon-docs` repo doesn't break it).

## Working Rules

1. Start from the subdirectory under `peon/` that directly owns the behavior; read its nested guide first.
2. Keep changes scoped to that subdirectory unless the task is explicitly cross-cutting.
3. If a change affects user-visible behavior, update `peon/docs/` source docs in the same pass.
4. Do not hand-edit generated artifacts under `peon/docs/manual/site/` or `the-peon-project.github.io/` unless explicitly asked for generated output.
5. Do not run deployment scripts that require `sudo`, shell profile mutation, or secret prompts unless explicitly asked for that operational step.
6. Do not start new work in `peon-orc/` (the one deprecated/archived directory still on disk) — migrate the equivalent change into `peon/` instead.

## Commands

Run commands from `peon/<subdirectory>` unless a task is explicitly workspace-wide.

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

These native/local commands are for iteration only (see **Deployment / Release Validation** below) — they are never a substitute for the docker compose flow when a feature is being shipped.

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

Only run the docs packaging script when the task includes rebuilding or publishing generated docs. It writes into `the-peon-project.github.io/`.

## Validation Expectations By Subdirectory

- `peon/services/webui/backend`: run `python3 -m pytest tests` if the change can affect backend behavior.
- `peon/services/webui/frontend`: run frontend tests when UI logic changes; if tests are not targeted enough, at minimum ensure the frontend build or test runner starts cleanly.
- `peon/services/orc`: no committed narrow automated suite was found; prefer targeted startup and syntax validation around touched files.
- `peon/services/bot-discord`: no committed narrow automated suite was found; prefer syntax validation and targeted module-level checks.
- `peon/cli`: validate shell changes with targeted script help or specific non-destructive flags.
- `peon/warplans`: validate JSON shape and keep the per-game README aligned with `plan.json` changes.
- `peon/docs`: validate source markdown and, when requested, rebuild via `./package_docs.sh`.

## Files Worth Knowing

- Deployment composition: `peon/config/docker-compose/`
- Orchestrator API: `peon/services/orc/app/modules/api_v1.py`
- Orchestrator bootstrap: `peon/services/orc/app/main.py`
- CLI entrypoint: `peon/cli/bin/peon`
- Warplan registry: `peon/warplans/plans.json`
- Web UI backend app: `peon/services/webui/backend/server.py`
- Web UI frontend package metadata: `peon/services/webui/frontend/package.json`
- Docs navigation and site config: `peon/docs/manual/zensical.toml`
- Docs publishing script: `peon/docs/package_docs.sh`

## High-Signal Change Patterns

### Adding or changing a game

Usually touches several subdirectories of `peon/`:

1. `peon/warplans/` for the game definition
2. `peon/wartable/` if a container or runtime image changes
3. `peon/services/orc/` if orchestration logic or API assumptions change
4. `peon/docs/` for development and user-facing documentation

### Changing server management behavior

Check impacts across:

1. `peon/services/orc/` for the actual control behavior
2. `peon/services/webui/` if the dashboard depends on the changed endpoint or payload
3. `peon/services/bot-discord/` if bot commands call the same API
4. `peon/cli/` if operator commands mirror the same action

### Changing deployment

Start in `peon/` and inspect the compose fragments in `config/docker-compose/` before editing `deploy_peon.sh` or any subdirectory's runtime assumptions.

## Deployment / Release Validation

**The docker compose flow is the only sanctioned way to build and ship a feature.** A feature is not shipped until it has been built into image(s) and deployed through `peon/deploy_peon.sh` (which composes the fragments in `peon/config/docker-compose/`) to the UAT/prod stack at `/home/richard/peon/`. Running a service natively (`python3 app/main.py`, `yarn start`, etc.), hand-copying files into `/home/richard/peon/`, or standing up containers outside this compose flow is for local iteration only and never counts as shipped.

For any task that includes deployment, release validation, or final runtime verification: build updated service image(s) from source under `/home/richard/development/peon`, then upgrade the UAT stack at `/home/richard/peon/` (a separate deployed instance from this dev workspace, reachable at `https://server.warcamp.org`) to those images via `peon/deploy_peon.sh`, and validate behavior against that upgraded UAT instance. Local unit/syntax checks are useful for iteration, but final sign-off for release-tagged work should be based on the upgraded UAT runtime. Only take this operational step when explicitly requested.

## Safety Notes

- `peon/deploy_peon.sh` is operational, interactive, and not safe as a routine validation step. It writes `.env`, updates `~/.bashrc`, writes `/etc/motd`, and starts containers.
- Do not request or paste secrets such as Discord tokens or production API keys into chat output.
- Prefer non-destructive validation first.

## Default Workflow

When no more specific instruction exists:

1. Determine the owning subdirectory under `peon/`.
2. Read only the local files needed to form a concrete hypothesis.
3. Make the smallest grounded edit.
4. Run the narrowest validation available for that subdirectory.
5. Update `peon/docs/` if behavior or developer workflow changed.

Repo-local guides also exist in (nested `CLAUDE.md`, or your tool's equivalent, per subdirectory):

- `peon/CLAUDE.md`
- `peon/services/orc/CLAUDE.md`
- `peon/services/webui/CLAUDE.md`
- `peon/services/bot-discord/CLAUDE.md`
- `peon/cli/CLAUDE.md`
- `peon/warplans/CLAUDE.md`
- `peon/wartable/CLAUDE.md`
- `peon/docs/CLAUDE.md`

Automatic file-pattern instructions also live in `.github/instructions/`.

## Deprecated repos (archived, read-only reference only)

- `peon-orc/` → superseded by `peon/services/orc/` — still on disk at the workspace root
- `peon-cli/` → superseded by `peon/cli/` — removed from disk
- `peon-warplans/` → superseded by `peon/warplans/` — removed from disk
- `peon-wartable/` → superseded by `peon/wartable/` — removed from disk
- `peon-webui/` → superseded by `peon/services/webui/` — removed from disk
- `peon-bot-discord/` → superseded by `peon/services/bot-discord/` — removed from disk
- `peon-docs/` → superseded by `peon/docs/` — removed from disk

All 7 GitHub repos are archived (read-only); `do-update` at the workspace root is the one-off script that pushed the deprecation-notice commits and archived them. Only `peon-orc/` remains checked out locally (kept so its commit history stays browsable without a remote fetch); the other 6 have already been deleted from this workspace.

## Knowledge graph (graphify)

This project has a knowledge graph at `graphify-out/` with god nodes, community structure, and cross-file relationships.

- For codebase questions, first run `graphify query "<question>"` when `graphify-out/graph.json` exists. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than `GRAPH_REPORT.md` or raw grep output.
- If `graphify-out/wiki/index.md` exists, use it for broad navigation instead of raw source browsing.
- Read `graphify-out/GRAPH_REPORT.md` only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).
