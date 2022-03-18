# PEON (Simple Game Server Manager)

An **OpenSource** project to assist gamers in self deploying/managing game servers.\
Intended to be a one-stop-shop for game server deployment/management.\
If run on a public/paid cloud, it is architected to try minimise costs (easy schedule/manage uptime vs downtime)\

## Architecture

WebUI (PeonUI) built into docker image using flask as base.
Docker compose to deploy all app components (PeonUI, PostgreSQL)

Flask provided by [tiangolo/uvicorn-gunicorn-fastapi-docker](https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker)\
Bootstrap provided by [bootswatch/darkly](https://bootswatch.com/darkly/)\
Postgres provided by [postgres:14-alpine](https://hub.docker.com/_/postgres)

### Feature Plan

#### *sprint 1*

- [ ] WebUI - Access controlled webpage for management
- [ ] Deploy and delete games from a recipe catalgue (hosted here)
- [ ] Start/stop servers with timeouts (e.g. specify a game session to run for 6 hours (with option to extend))

#### *sprint 2*

- [ ] Recipes - Autodetect newly added recipies.
- [ ] Persistent server data - Keep server data for updates & future releases.

#### *sprint 3*

- [ ] RESTful API control (for things like discord bots)

#### Notes

[Flask app example](https://ianlondon.github.io/blog/deploy-flask-docker-nginx/)

Quick Project Download

```bash
wget https://github.com/nox-noctua-consulting/peon/archive/main.zip
```

Deploy app in Detached mode

```bash
docker-compose up -d
```

## Implemented so far

1. **Docker Image** Can build/deploy flask app into custom docker image
2. **Docker Compose** Can deploy webui.webapp and webui.db using ``docker-compose up -d``, with app only starting after db has started.
