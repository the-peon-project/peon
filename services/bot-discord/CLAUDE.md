# PEON Discord Bot Guide

This repo contains the Discord bot interface for PEON.

## Scope

- Main bot entrypoint: `app/main.py`
- Discord command and UI helpers: `app/modules/`
- Runtime dependencies: `requirements.txt`

## Runtime Map

- Language/runtime: Python + `discord.py`
- Main startup: `python3 app/main.py`
- Startup syncs slash commands and performs channel cleanup
- The bot depends on orchestrator connectivity for server and plan operations

## Working Rules

1. Start from the slash command or module that directly owns the behavior.
2. Preserve Discord permission assumptions, autocomplete behavior, and startup sync behavior unless the task requires changing them.
3. Treat secrets and tokens as terminal-only input; never ask for them in chat.
4. If command behavior changes, inspect likely API assumptions against `peon-orc`.
5. If user-visible bot workflows change, update `peon-docs/` source docs.

## Commands

```bash
cd /home/richard/development/peon-bot-discord
python3 -m pip install -r requirements.txt
python3 app/main.py
```

Safe validation:

```bash
cd /home/richard/development/peon-bot-discord
python3 -m py_compile app/main.py
```

## Important Files

- Bot startup and slash commands: `app/main.py`
- Admin flows: `app/modules/administrator.py`
- Orchestrator integration: `app/modules/orchestrator.py`
- User flows: `app/modules/user.py`
- Shared helpers: `app/modules/shared.py`
- Repo dependencies: `requirements.txt`

## Validation Expectations

- Prefer syntax validation and narrow module-level checks
- Avoid runtime startup if it would require missing secrets or live Discord side effects
- If runtime validation is needed and a token is missing, ask the user to provide it directly in the terminal

## Cross-Repo Dependencies

- Depends on `peon-orc` for orchestrator and server actions
- User-visible workflows should stay aligned with `peon-docs/`
- Plan discovery behavior can be affected by `peon-warplans/`

## Default Workflow

1. Find the owning slash command or helper module.
2. Read the integration path into orchestrator helpers.
3. Make the smallest safe edit.
4. Run syntax validation first.
5. Update docs if command behavior or setup expectations changed.