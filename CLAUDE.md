# PEON Deployment Meta-Repo Guide

This repo composes the PEON stack and owns deployment wiring. Treat it as the place for stack composition, not day-to-day feature logic.

## Scope

- Main deployment script: `deploy_peon.sh`
- Compose fragments: `config/docker-compose/`
- Orchestrator registry/config: `config/peon.orchestrators.json`

## Working Rules

1. Use this repo when changing deployment composition, environment wiring, or which services are enabled together.
2. Read the compose fragments before changing `deploy_peon.sh`.
3. Treat `deploy_peon.sh` as operationally sensitive: it writes `.env`, updates `~/.bashrc`, writes `/etc/motd`, and starts containers.
4. Do not use deployment as routine validation unless the user explicitly asked for that operational step.
5. If deployment behavior changes, update `peon-docs/` source docs.

## Important Files

- Interactive deployment entrypoint: `deploy_peon.sh`
- Compose fragments: `config/docker-compose/01_network.yml`, `02_orc.yml`, `03_webui.yml`, `05_docs.yml`, `20_bots.yml`
- Orchestrator config: `config/peon.orchestrators.json`

## Validation Expectations

- Prefer static review of compose fragments and environment wiring first.
- If a shell change is made, use `bash -n deploy_peon.sh` before considering any operational execution.
- Avoid running the deployment script unless the user explicitly wants deployment performed.

## Cross-Repo Dependencies

- Wires together `peon-orc`, `peon-webui`, `peon-docs`, and `peon-bot-discord`
- Deployment changes can affect the entire runtime workspace

## Default Workflow

1. Start from the affected compose fragment or deployment step.
2. Make the smallest deployment-focused change.
3. Validate statically or with shell syntax checks first.
4. Update docs if stack setup behavior changed.