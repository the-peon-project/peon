# PEON (Play Everything On Nodes)

## The Easy Game Server Manager

An **OpenSource** project to assist gamers in self deploying/managing game servers.\
Intended to be a one-stop-shop for game server deployment/management.\
If run on a public/paid cloud, it is architected to try minimise costs (easy schedule/manage uptime vs downtime)

## Architecture

- [Peon WebUI (peon.ui)](https://github.com/nox-noctua-consulting/peon-ui) - WebUI for automation
- [Peon Orchestrator (peon.orc)](https://github.com/nox-noctua-consulting/peon-orc) - REST controlled server automation
- [Peon Plans](https://github.com/nox-noctua-consulting/peon-plans) - Game server plans & recipies

### Feature Plan

#### *sprint 0.1.0*

- [x] peon-cli - A cli component for backend server support, which runs on the host.
- [ ] WebUI - Access controlled webpage for management
- [ ] Deploy and delete games from a recipe catalgue (hosted at [Peon Recipies](https://github.com/nox-noctua-consulting/peon-recipies))
- [x] REST controlled deploy/start/stop servers

#### *sprint 0.2.0*

- [ ] Recipes - Autodetect newly added recipies.
- [ ] Persistent server data - Keep server data for updates & future releases.

#### *sprint 0.3.0*

- [ ] Public RESTful API control (for things like discord bots)
- [ ] Server file backups

#### Notes

[Flask app example](https://ianlondon.github.io/blog/deploy-flask-docker-nginx/)

## How To

### Requirements

Please note that the requirements will change/improve over time.

- [Docker] running on a server
- [Internet] connection to be able to reach github & docker hub.
- [SSH Server] running on the docker host (allowing access on port ``22222``)

### Deployment

#### 1. Working directory

Create a working directory for the project

```bash
mkdir /root/peon
```

#### 2. Download latest release

Pull the latest release from the peon repo

```bash
wget https://github.com/nox-noctua-consulting/peon/archive/refs/tags/warcamp.tar.gz
```

#### 3. Extract the project

Extract the project files into the ``peon`` directory.

```bash
tar -xvf warcamp.tar.gz --strip-components=1 --directory peon -C /root/peon/.
```

#### 4. Deploy Peon to server

Run download/deploy containers and configure services.

```bash
./install_peon.sh
```

#### 5. Run ``peon-cli`` to confirm health (optional)

A management tui which runs on the docker host and is used to streamline peon support.

```bash
peon-cli
```
