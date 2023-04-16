# Orchestrator

- [ ] CHANGE :tools: Change to svn download for directory (plans)

## v.0.3.2

- [x] ADDED :new: Added `/app/bin` to path and added `peon` cli module into orc.
- [x] CHANGE :tools: Make API key configurable

## v0.3.1

- [x] CHANGE :tools: Rework Orcestrator app to leverage the `docker.sock`
- [x] CHANGE :tools: Moving to init script `init/peon.orc`, for pre-flight checks.
- [x] REMOVED :scissors: Removed SSH check on boot from `python3 main.py`
- [x] ADDED :new: Configurable docker socket path.
- [x] ADDED :new: Added `VERSION` environment variable into container.

## v0.3.0

- [x] CHANGE :tools: Change dockerfile to support using `docker.sock` socket file to manage docker (from SSH)

## v0.2.17-dev

- [x] BUGFIX :beetle: Remove schedule on manual stop
- [x] CHANGE :tools: Validate epoch time input for scheduler epoch time

## v0.2.16-dev

- [x] BUGFIX :beetle: Server create returned false error due to change error dict hanlder

## v0.2.15-dev

- [x] BUGFIX :beetle: Scheduler vs Start/Stop

## v0.2.14-dev

- [x] BUGFIX :beetle: Scheduler v1.0 - Bugfix (server stop is now properly scheduled)

## v0.2.13-dev

- [x] ADDED :new: Scheduler - v1.0 - Added simple start & delayed stop in scheduler

## v0.2.12-dev

- [x] CHANGE :tools: API Response - Server config

## v0.2.11-dev

- [x] ADDED :new: PUBLIC_IP - added to container variables

## v0.2.10-dev

- [x] Logging - Added devMode switch

## v0.2.9-dev

- [x] ADDED :new: UI - Added MOTD to container login

## v0.2.8-dev

- [x] CHANGE :tools:  Base images were repulled to get latest versions & app rebuilt on those
- [x] BUGFIX :beetle: Incorrect parameter reference in server create

## v0.2.7-dev

- [x] SECURITY :unlock: Inital CORS implementation
- [x] SECURITY :unlock: Initial api-key requirement implementation

## v0.2.6-dev

- [x] ADDED :new: API - Server - Destroy & Eradicate

## v0.2.5-dev

- [x] ADDED :new: API - Server - Reworked to include actions into path
- [x] ADDED :new: API - Server - Added get with metrics

## v0.2.4-dev

- [x] ADDED :new: API - Server Get - reworked to provide both container & server state

## v0.2.3-dev

- [x] ADDED :new: API - Auto download latest plan version when server is deployed

## v0.2.2-dev

- [x] ADDED :new: API - Plans get list & update from Peon project list

## v0.2.1-dev

- [x] BUGFIX :beetle: Enforced description & settings on [post]servers

## v0.2.0-dev

- [x] ADDED :new: Added custom config handler
- [x] CHANGE :tools: Allows configuration of environment variables in container (via API)
- [x] ADDED :new: Can supply json/txt files via API
- [x] ADDED :new: Added persistent description

## v0.1.6-dev

- [x] ADDED :new: Added handler for `config` folder
- [x] ADDED :new: Moved game server logs into game server directory

## v0.1.5-dev

- [x] INITIALISED :airplane:  First iteration of server create (API)
