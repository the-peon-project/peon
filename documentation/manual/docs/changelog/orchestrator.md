# Orchestrator

- Rework Orcestrator app to leverage the socker file

## v0.3.0

- Changed dockerfile to support using `docker.sock` socket file to manage docker (from SSH)

## v0.2.17-dev

- Bug Fixes - Remove schedule on manual stop
- Improvement - Validate epoch time input for scheduler epoch time

## v0.2.16-dev

- Bug Fixes - Server create returned false error due to change error dict hanlder

## v0.2.15-dev

- Bug Fixes - Scheduler vs Start/Stop

## v0.2.14-dev

- Scheduler v1.0 - Bugfix (server stop is now properly scheduled)

## v0.2.13-dev

- Scheduler - v1.0 - Added simple start & delayed stop in scheduler

## v0.2.12-dev

- API Response - Server config

## v0.2.11-dev

- PUBLIC_IP - added to container variables

## v0.2.10-dev

- Logging - Added devMode switch

## v0.2.9-dev

- UI - Added MOTD to container login

## v0.2.8-dev

- Base Image Update - Base images were repulled to get latest versions & app rebuilt on those
- BugFix: Incorrect parameter reference in server create
  
## v0.2.7-dev

- Security - Inital CORS implementation
- Security - Initial api-key requirement implementation

## v0.2.6-dev

- API - Server - Destroy & Eradicate

## v0.2.5-dev

- API - Server - Reworked to include actions into path
- API - Server - Added get with metrics

## v0.2.4-dev

- API - Server Get - reworked to provide both container & server state

## v0.2.3-dev

- API - Auto download latest plan version when server is deployed
  
## v0.2.2-dev

- API - Plans get list & update from Peon project list

## v0.2.1-dev

- Bugfix - Enforced description & settings on [post]servers
  
## v0.2.0-dev

- Added custom config handler
- Allows configuration of environment variables in container (via API)
- Can supply json/txt files via API
- Added persistent description

## v0.1.6-dev

- Added handler for ``config`` folder
- Moved game server logs into game server directory

## v0.1.5-dev

- First iteration of server create (API)
