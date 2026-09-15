# Peon War Plan - Windrose

The PEON war plan that Peon uses to deploy your game server.

> **Windrose dedicated server is distributed as a Steam tool (app id `4129620`) and currently ships as a Windows server binary. This plan uses the PEON `steamcmd-proton:1.2.16` image to keep PEON runtime integrations (`state`, `ip`, and server config files) available through the API.**

## Documentation

If you would like info on how to use this plan, the up-to-date documentation can be found in the [PEON project game guide](http://docs.warcamp.org/guides/games/windrose/).

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/K3K567ILJ)

## Stand-alone Use

This recipe can be used without the wider PEON project components.

### Guide

For this guide, please make sure you have [Docker Compose](https://docs.docker.com.zh.xy2401.com/v17.12/compose/install/) installed and running.

1. Download this folder and its contents.
2. Create a file `docker-compose.yml` in the directory with the contents as below.
3. Ensure that any scripts in the directory are executable by the docker user.
4. Start the server using `docker-compose up -d` / `docker compose up -d`.

#### docker-compose.yml

```yml
services:
  server:
    container_name: peon.warcamp.windrose.default
    hostname: peon.warcamp.windrose
    image: umlatt/steamcmd-proton:1.2.16
    ports:
      - 7777:7777/tcp
      - 7777:7777/udp
    environment:
      - PORT=7777
      - STEAM_ID=4129620
      - SERVER_NAME=windrose
      - PASSWORD=
      - MAX_PLAYERS=8
    volumes:
      - ./actions:/actions
      - ./data:/home/steam/steamcmd/data
      - ./config:/home/steam/config
      - ./user:/home/steam/steamcmd/data/R5/Saved
    user: 1000:1000
```
