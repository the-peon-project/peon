# PEON Warplans Guide

This directory defines supported games and their deployment recipes. Treat each game directory as a discrete configuration surface. Formerly the standalone `peon-warplans` repo, now `peon/warplans/` in the consolidated `peon` monorepo (see the root `CLAUDE.md` for the overall map).

## Scope

- Registry of supported games: `plans.json`
- Per-game configuration: `<game>/plan.json`
- Per-game documentation: `<game>/README.md`
- Per-game helper assets: `<game>/actions/`, optional `data/`, and logos
- One-off migration tooling: `tools/` (e.g. `migrate_server_start.py`, used to extract the shared `server_start` boilerplate into the sourced library — see the note under Cross-Directory Dependencies)

## Structure

Each supported game normally follows this pattern:

```text
<game>/
  plan.json
  README.md
  actions/
```

Some games also carry additional assets such as `data/`.

`plans.json` entries point `plan_url` at `https://github.com/the-peon-project/peon/tree/main/warplans/<game_uid>` — the monorepo path, not a standalone repo URL. This is already updated; do not edit `plans.json` as part of routine per-game work.

## Working Rules

1. Keep `plans.json` aligned with per-game directories.
2. Keep each game's `README.md` aligned with its `plan.json` when behavior changes.
3. Treat `metadata.mode`, image references, ports, environment variables, and mounted volumes as externally significant contract points.
4. If a plan change implies a new runtime image or base behavior, inspect `peon/wartable/containers/`.
5. If orchestration assumptions change, inspect `peon/services/orc/`.
6. If user-facing setup or supported-game docs change, update `peon/docs/` source docs.
7. Keep changes minimal and directory-local unless the task is explicitly cross-directory.
8. Prefer non-destructive validation first; do not request or print secrets, and do not edit generated docs outputs directly.

## Commands

No build or run commands apply to this directory directly; validation is limited to JSON/document checks (see below).

## Validation Expectations

- Validate `plans.json` and each touched `plan.json` with `python -m json.tool`.
- Confirm referenced sibling paths such as `actions/` or `data/` actually exist.
- Confirm the game stays present and correctly named in `plans.json`.
- Prefer targeted checks over broad repo-wide rewrites.
- The docker compose flow is the only sanctioned way to build and ship a feature — never treat a native run or a hand-copied file as shipped. For deployment or release validation, build updated images from source under `/home/richard/development/peon`, then upgrade the UAT/prod stack at `/home/richard/peon/` (a separate deployed instance, distinct from this dev checkout — reachable at `https://server.warcamp.org`) via `peon/deploy_peon.sh` before sign-off — do not run this as routine validation.

## Important Files

- Global registry: `plans.json`
- Example game plan: `valheim/plan.json`
- Example game docs: `valheim/README.md`

## Cross-Directory Dependencies (within this repo)

- `peon/services/orc` consumes these plans to create and manage servers. Since a real deployment host is typically a thin checkout without `warplans/`, orc's `app/modules/github.py` clones `https://github.com/the-peon-project/peon.git` and sparse-checks-out this directory into a runtime `plans/` directory (mounted into the orc container at `/home/peon/plans` via `config/docker-compose/02_orc.yml`) — see `services/orc/CLAUDE.md`'s "Warplan Source" section for the full mechanism. Changes made here take effect for the orchestrator once merged to `main` (the fetch pulls from `github.com/the-peon-project/peon.git`'s `main` branch, not from a local working tree), on the next `PUT /api/v1/plans` refresh or orc container restart with an empty `plans/` directory.
- `<game>/actions/server_start` scripts may `source` a shared helper library baked into the wartable base image at `/init/lib/server_start_lib.sh` (see `peon/wartable/CLAUDE.md`); the migrated scripts guard this with an existence check so they still work when run against an image that predates that base image.
- `peon/wartable` may need updates when modes or images change.
- `peon/docs` should reflect supported games and configuration behavior.

## Default Workflow

1. Start with the specific game directory.
2. Read `plan.json` and the sibling `README.md`.
3. Make the smallest valid configuration change.
4. Validate JSON shape and referenced assets.
5. Update docs in this directory and `peon/docs/` as needed.
