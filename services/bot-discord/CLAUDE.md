# PEON Discord Bot Guide

This directory owns the Discord bot interface for PEON. Formerly the standalone `peon-bot-discord` repo, now `peon/services/bot-discord/` in the consolidated `peon` monorepo (see the root `CLAUDE.md` for the overall map).

## Scope

- Main bot entrypoint: `app/main.py`
- Discord command and UI helpers: `app/modules/`
- Config: `app/config/`
- Reference data: `app/reference/`
- Tests: `tests/test_server_channel_parsing.py`
- Runtime dependencies: `requirements.txt`

## Runtime Map

- Language/runtime: Python + `discord.py`
- Main startup: `python3 app/main.py`
- Startup syncs slash commands and performs channel cleanup
- The bot depends on orchestrator connectivity for server and plan operations

## Working Rules

1. Start from the slash command or module that directly owns the behavior.
2. Keep changes minimal and local to this directory unless the task is explicitly cross-directory.
3. Preserve Discord permission assumptions, autocomplete behavior, and startup sync behavior unless the task requires changing them.
4. Treat secrets and tokens as terminal-only input; never request or print them in chat.
5. Use non-destructive validation first.
6. If command behavior changes, inspect likely API assumptions against `peon/services/orc`.
7. If user-visible bot workflows change, update `peon/docs/` source docs.
8. Do not edit generated docs outputs directly.
9. The docker compose flow is the only sanctioned way to build and ship a feature — running `python3 app/main.py` locally is for iteration only and never counts as shipped. For deployment or release validation, build updated images from source under this directory, then upgrade the UAT/prod stack at `/home/richard/peon/` (a separate deployed instance, distinct from this dev checkout — reachable at `https://server.warcamp.org`) via `peon/deploy_peon.sh` before sign-off.

## Commands

```bash
cd /home/richard/development/peon/services/bot-discord
python3 -m pip install -r requirements.txt
python3 app/main.py
```

Safe validation:

```bash
cd /home/richard/development/peon/services/bot-discord
python3 -m py_compile app/main.py
```

## Important Files

- Bot startup and slash commands: `app/main.py`
- Admin flows: `app/modules/administrator.py`
- Orchestrator integration: `app/modules/orchestrator.py`
- User flows: `app/modules/user.py`
- Shared helpers: `app/modules/shared.py`
- Config: `app/config/`
- Reference data: `app/reference/`
- Tests: `tests/test_server_channel_parsing.py`
- Directory dependencies: `requirements.txt`

## Validation Expectations

- Prefer narrow Python syntax checks and targeted module-level validation.
- Avoid runtime startup if it would require missing secrets or live Discord side effects.
- If runtime validation is needed and a token is missing, ask the user to provide it directly in the terminal.

## Cross-Directory Dependencies (within this repo)

- Depends on `peon/services/orc` for orchestrator and server actions
- Plan discovery behavior can be affected by `peon/warplans`
- User-visible workflows should stay aligned with `peon/docs`

## Default Workflow

1. Find the owning slash command or helper module.
2. Read the integration path into orchestrator helpers.
3. Make the smallest safe edit.
4. Run syntax validation first.
5. Update docs if command behavior or setup expectations changed.
