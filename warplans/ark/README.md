# Peon War Plan - Ark

The PEON war plan that Peon uses to deploy your game server.

![Ark](./logo.png)

## Documentation

If you would like info on how to use this plan, the up-to-date documentation can be found in the [PEON project game guide](http://docs.warcamp.org/guides/games/ark/).

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
        container_name: peon.warcamp.ark.servername
        hostname: peon.warcamp.ark.servername
        image: umlatt/steamcmd
        ports:
        - 7777:7777/udp
        - 7778:7778/udp
        - 27015:27015/udp
        - 27020:27020/udp
        environment:
        - PORT=7777
        - RAWPORT=7778
        - QUERYPORT=27015
        - RCON=27020
        - STEAM_ID=376030
        - SERVER_NAME=YOUR-SERVER-NAME
        - ADMIN_PASSWORD=YOUR-SERVER-ADMIN-PASSWORD
        - PASSWORD=YOUR-SERVER-PASSWORD
        volumes:
        - ./actions:/actions
        - ./data:/home/steam/steamcmd/data
        - ./config:/home/steam/config
        - ./user:/home/steam/steamcmd/data/ShooterGame/Saved
        user: 1000:1000
```
