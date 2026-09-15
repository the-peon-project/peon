# Peon Warplan - Duke Nukem 3D (EDuke32)

The PEON war plan that Peon uses to deploy a Duke Nukem 3D multiplayer game server using the EDuke32 source port.

![DukeNukem3D](./logo.png)

## Documentation

If you would like info on how to use this plan, the up-to-date documentation can be found in the [PEON project game guide](http://docs.warcamp.org/).

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/K3K567ILJ)

## Important: Game Data Required

You **must** provide a legal copy of `DUKE3D.GRP` from your Duke Nukem 3D installation. Place it in the `data/` directory before starting the server.

You can obtain `DUKE3D.GRP` from:
- [Duke Nukem 3D: 20th Anniversary World Tour](https://store.steampowered.com/app/434050/) on Steam
- An original Duke Nukem 3D CD-ROM

## Notes

- EDuke32 multiplayer is considered experimental. Network propagation of destructible walls and doors may not work perfectly.
- Default port is **23513/udp**.
- Clients must connect using EDuke32 with matching game data.

## Stand-alone Use

This recipe can be used without the wider PEON project components.

### Guide

For this guide, please make sure you have [Docker Compose](https://docs.docker.com.zh.xy2401.com/v17.12/compose/install/) installed and running.

1. Download this folder and its contents.
2. Place your `DUKE3D.GRP` file in a `data/` subdirectory.
3. Create a file `docker-compose.yml` in the directory with the contents as below.
4. Ensure that any scripts in the directory (i.e. `server_start`, `init_custom`) are executable by the docker user.
    ```bash
    chown 1000:1000 actions/*
    chmod u+x actions/*
    ```
5. Start the server with `docker compose up -d`. Follow the deployment using `docker compose logs -f`.

### docker-compose.yml

```yml
version: "3"
services:
  dukenukem:
    image: umlatt/steamcmd
    ports:
      - "23513:23513/udp"
    environment:
      - SERVER_NAME=MyDukeServer
      - MAX_PLAYERS=8
      - PORT=23513
    volumes:
      - ./actions:/actions
      - ./data:/home/steam/steamcmd/data
      - ./config:/home/steam/config
    restart: unless-stopped
```
