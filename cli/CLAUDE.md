# PEON CLI Guide

This directory owns the host-side shell CLI for managing a PEON installation. It is an operator-facing wrapper around the deployed PEON containers, not a service itself. Formerly the standalone `peon-cli` repo, now `peon/cli/` in the consolidated `peon` monorepo (see the root `CLAUDE.md` for the overall map).

## Scope

- Main entrypoint: `bin/peon`
- Shared shell helpers: `bin/modules/shared.sh`
- PEON infrastructure actions: `bin/modules/peon.sh`
- Game/container actions: `bin/modules/game.sh`
- Supporting scripts: `bin/connect`, `bin/logs`, `bin/test_port`

## Runtime Map

- Language/runtime: Bash
- Primary interface: interactive menu plus flag-driven commands
- Depends on Docker being available on the host
- Stores the configured PEON root path in `bin/config/peon_dir`

## Working Rules

1. Start from the flag path or helper function that actually performs the action.
2. Preserve non-interactive usage when editing menu logic.
3. Treat commands that stop, restart, redeploy, or kill containers as operationally sensitive.
4. Prefer validating with `--help` or other non-destructive flags first.
5. Keep changes minimal and directory-local unless the task is explicitly cross-directory.
6. If CLI behavior changes, check whether docs in `peon/docs/` should also change.
7. Do not request or print secrets.
8. Do not edit generated docs outputs directly.
9. For deployment or release validation, build updated images from source under `/home/richard/development` and deploy through `/home/richard/peon` (the deployed instance, distinct from this development checkout) before sign-off.

## Commands

```bash
cd /home/richard/development/peon/cli
bash bin/peon --help
```

## Safe Validation

- For flag handling or dispatch changes: run `bash bin/peon --help`.
- For shell syntax changes: run `bash -n` against the touched scripts, e.g. `bash -n bin/peon`.
- Avoid destructive command paths (stop/restart/redeploy/kill) unless the user explicitly requested operational validation.

```bash
cd /home/richard/development/peon/cli
bash bin/peon --help
bash -n bin/peon
```

## Important Files

- Main dispatcher: `bin/peon`
- Shared shell helpers: `bin/modules/shared.sh`
- PEON operations: `bin/modules/peon.sh`
- Game operations: `bin/modules/game.sh`
- Connection/logging/port helpers: `bin/connect`, `bin/logs`, `bin/test_port`

## Cross-Directory Dependencies (within this repo)

- Targets deployed PEON infrastructure composed from the repo root (`peon/`, `deploy_peon.sh`, `config/docker-compose/`).
- Mirrors operational behavior exposed by `peon/services/orc`.
- User-facing workflow changes should be reflected in `peon/docs`.

## Default Workflow

1. Identify the relevant CLI flag or menu action.
2. Step into the helper module that implements it.
3. Make the smallest shell change needed.
4. Run shell syntax or help-path validation.
5. Update `peon/docs` if operator behavior changed.
