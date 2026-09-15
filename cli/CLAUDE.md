# PEON CLI Guide

This repo contains the host-side shell CLI for managing a PEON installation.

## Scope

- Main entrypoint: `bin/peon`
- Shared shell helpers: `bin/modules/shared.sh`
- PEON infrastructure actions: `bin/modules/peon.sh`
- Game/container actions: `bin/modules/game.sh`

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
5. If CLI behavior changes, check whether docs in `peon-docs/` should also change.

## Commands

```bash
cd /home/richard/development/peon-cli
bash bin/peon --help
```

Common safe validations:

```bash
cd /home/richard/development/peon-cli
bash bin/peon --help
bash -n bin/peon
```

## Important Files

- Main dispatcher: `bin/peon`
- Shared shell helpers: `bin/modules/shared.sh`
- PEON operations: `bin/modules/peon.sh`
- Game operations: `bin/modules/game.sh`

## Validation Expectations

- For flag handling or dispatch changes: run `bash bin/peon --help`
- For shell syntax changes: run `bash -n` against the touched scripts
- Avoid destructive command paths unless the user explicitly requested operational validation

## Cross-Repo Dependencies

- Targets deployed PEON infrastructure from `peon/`
- Mirrors operational behavior exposed by `peon-orc`
- User-facing workflow changes should be reflected in `peon-docs/`

## Default Workflow

1. Identify the relevant CLI flag or menu action.
2. Step into the helper module that implements it.
3. Make the smallest shell change needed.
4. Run shell syntax or help-path validation.
5. Update docs if operator behavior changed.