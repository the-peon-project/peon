# PEON Warplans Guide

This repo defines supported games and their deployment recipes. Treat each game directory as a discrete configuration surface.

## Scope

- Registry of supported games: `plans.json`
- Per-game configuration: `<game>/plan.json`
- Per-game documentation: `<game>/README.md`
- Per-game helper assets: `<game>/actions/`, optional `data/`, and logos

## Structure

Each supported game normally follows this pattern:

```text
<game>/
  plan.json
  README.md
  actions/
```

Some games also carry additional assets such as `data/`.

## Working Rules

1. Keep `plans.json` aligned with per-game directories.
2. Keep each game's `README.md` aligned with its `plan.json` when behavior changes.
3. Treat `metadata.mode`, image references, ports, environment variables, and mounted volumes as externally significant contract points.
4. If a plan change implies a new runtime image or base behavior, inspect `peon-wartable/containers/`.
5. If orchestration assumptions change, inspect `peon-orc/`.
6. If user-facing setup or supported-game docs change, update `peon-docs/` source docs.

## Validation Expectations

- Confirm changed `plan.json` files remain valid JSON.
- Confirm referenced sibling paths such as `actions/` or `data/` actually exist.
- Confirm the game stays present and correctly named in `plans.json`.
- Prefer targeted checks over broad repo-wide rewrites.

## Important Files

- Global registry: `plans.json`
- Example game plan: `valheim/plan.json`
- Example game docs: `valheim/README.md`

## Cross-Repo Dependencies

- `peon-orc` consumes these plans to create and manage servers
- `peon-wartable` may need updates when modes or images change
- `peon-docs` should reflect supported games and configuration behavior

## Default Workflow

1. Start with the specific game directory.
2. Read `plan.json` and the sibling `README.md`.
3. Make the smallest valid configuration change.
4. Validate JSON shape and referenced assets.
5. Update docs in this repo and `peon-docs/` as needed.