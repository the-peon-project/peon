# Peon War Plan - Satisfactory

The PEON war plan that Peon uses to deploy your game server.

![Satisfactory](./logo.png)

## Documentation

If you would like info on how to use this plan, the up-to-date documentation can be found in the [PEON project game guide](http://docs.warcamp.org/guides/games/satisfactory/).

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/K3K567ILJ)

## Stand-alone Use

This recipe can be used without the wider PEON project components.

### Guide

For this guide, please make sure you have [Docker Compose](https://docs.docker.com.zh.xy2401.com/v17.12/compose/install/) installed and running.

1. Download this folder and its contents.
2. Create a file `docker-compose.yml` in the directory with the contents below.
3. Ensure that any scripts in the directory (i.e. `server_start`, `init_custom`) are executable by the docker user.
    ```bash
    chown 1000:1000 server_start
    chmod u+x server_start
    ```
4. Start the server. You can now start the server with the following command `docker-compose up -d`/`docker compose up -d`. You can then follow the deployment using `docker-compose logs -f`

#### docker-compose.yml

You can change any of the settings according to your needs.

```yml

services:
  server:
    container_name: peon.warcamp.satisfactory.default
    hostname: peon.steamcmd.satisfactory
    image: umlatt/steamcmd
    ports:
      - 15777:15777/udp
      - 15000:15000/udp
      - 7777:7777/udp
    environment:
      - STEAMID=1690800
      # GAME SERVER VARIABLES
      - SERVER_NAME=server01
    volumes:
      - ./actions:/actions
      - ./data:/home/steam/steamcmd/data
      - ./config:/home/steam/config
      - ./user:/home/steam/.config/Epic/FactoryGame/Saved/SaveGames
```
