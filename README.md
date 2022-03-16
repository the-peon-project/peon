# Federer (Game Server Manager)

A project to assist gamers in self deploying/managing game servers.

## Architecture

WebUI (FedererUI) built into docker image using flask as base.\
Docker compose to deploy all app components (FederUI, PostgreSQL)

Flask provided by [tiangolo/uwsgi-nginx-flask](https://hub.docker.com/r/tiangolo/uwsgi-nginx-flask/)\
Postgres provided by [postgres:14-alpine](https://hub.docker.com/_/postgres)

### Features

- Deploy and delete games from a recipe catalgue (hosted here)
- Start/stop servers with timeouts (e.g. specify a game session to run for 6 hours (with option to extend))
- Access control
- API control (for discord bots)
- Recipe checker
- Timers
- Persistent saves (UI managed)


#### Notes

[Flask app example](https://ianlondon.github.io/blog/deploy-flask-docker-nginx/)

Quick Project Download

```bash
wget https://github.com/nox-noctua-consulting/federer/archive/main.zip
```

Deploy app in Detached mode

```bash
docker-compose up -d
```
