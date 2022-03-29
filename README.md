# PEON (Pretty Epic Opensource Narcolepsy)

## The Easy Game Server Manager

An **OpenSource** project to assist gamers in self deploying/managing game servers.\
Intended to be a one-stop-shop for game server deployment/management.\
If run on a public/paid cloud, it is architected to try minimise costs (easy schedule/manage uptime vs downtime)\

## Architecture

- [Peon WebUI (peon.ui)](https://github.com/nox-noctua-consulting/peon-ui) - WebUI for automation
- [Peon Orchestrator (peon.orc)](https://github.com/nox-noctua-consulting/peon-orc) - REST controlled server automation
- [Peon Plans](https://github.com/nox-noctua-consulting/peon-plans) - Game server plans & recipies

### Feature Plan

#### *sprint 1.0.0*

- [x] peon-cli - A cli component for backend server support, which runs on the host.
- [ ] WebUI - Access controlled webpage for management
- [ ] Deploy and delete games from a recipe catalgue (hosted at [Peon Recipies](https://github.com/nox-noctua-consulting/peon-recipies))
- [ ] REST controlled deploy/start/stop servers

#### *sprint 2.0.0*

- [ ] Recipes - Autodetect newly added recipies.
- [ ] Persistent server data - Keep server data for updates & future releases.

#### *sprint 3.0.0*

- [ ] Public RESTful API control (for things like discord bots)
- [ ] Server file backups
#### Notes

[Flask app example](https://ianlondon.github.io/blog/deploy-flask-docker-nginx/)

##### Quick Project Download

```bash
wget https://github.com/nox-noctua-consulting/peon/archive/main.zip
```

##### Deploy app in Detached mode

```bash
docker-compose up -d
```

##### peon-cli
A management tui which runs on the docker host and is used to streamline peon support.
```bash
peon-cli
```

