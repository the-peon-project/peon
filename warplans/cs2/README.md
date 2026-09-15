# CS2

The PEON war plan that Peon uses to deploy a CS2 game server with minimal effort. *\*Configuring the server on the other hand... is admin, but we don't have control of that*

![CS:GO](./logo.png)

## Documentation

If you would like info on how to use this plan, the up-to-date documentation can be found in the [PEON project game guide](http://docs.warcamp.org/guides/games/cs2/).

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/K3K567ILJ)

## Stand-alone Use

This recipe can be used without the wider PEON project components.

### Guide

For this guide, please make sure you have [Docker Compose](https://docs.docker.com.zh.xy2401.com/v17.12/compose/install/) installed and running.

1. Download this folder and its contents.
2. Create a file `docker-compose.yml` in the directory with the contents as below.
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
        container_name: peon.warcamp.cs2.cliffstone
        hostname: peon.warcamp.cs2.cliffstone
        image: umlatt/steamcmd
        ports:
        - 27015:27015/tcp
        - 27015:27015/udp
        - 27020:27020/udp
        environment:
        - CS2_PORT=27015                              # CS2 server listen port tcp_udp.
        - TV_PORT=27020                               # SourceTV/CSTV port to bind to.
        - STEAM_ID=730                                # Steam app ID.
        - SERVER_NAME=cliffstone                      # Set the visible name for your private server.
        - STEAM_GSLT=01065FAC742AF7185C988A2C8F592A95 # Game Server Token from https://steamcommunity.com/dev/managegameservers.
        - STEAMAPP=cs2                                # Steam game.
        - STEAMAPPDIR=/home/steam/steamcmd/data       # Steam game installed dir.
        - STEAMAPPVALIDATE=0                          # Validate game files. (0=No, 1=Yes)
        - CS2_CHEATS=0                                # Enable cheats. (0=No, 1=Yes)
        - CS2_SERVER_HIBERNATE=0                      # Save CPU resources when no players connected. (0=No, 1=Yes)
        - CS2_RCON_PORT=                              # Optional, use a simple TCP proxy to have RCON listen on an alternative port. For services like AWS Fargate which do not support mixed protocol ports.
        - CS2_LAN=0                                   # Lan mode enabled. (0=No, 1=Yes)
        - CS2_RCONPW=                                 # RCON password.
        - CS2_PW=                                     # CS2 server password.
        - CS2_MAXPLAYERS=10                           # Max players allowed.
        - CS2_ADDITIONAL_ARGS=                        # Optional additional arguments to pass into cs2.
        - CS2_CFG_URL=                                # HTTP/HTTPS URL to fetch a Tar Gzip bundle of configuration files/mods.
        - CS2_GAMEALIAS=                              # Game type, e.g. casual, competitive, deathmatch.
        - CS2_GAMETYPE=0                              # Used if CS2_GAMEALIAS not defined. See https://developer.valvesoftware.com/wiki/Counter-Strike_2/Dedicated_Servers.
        - CS2_GAMEMODE=1                              # Used if CS2_GAMEALIAS not defined. See https://developer.valvesoftware.com/wiki/Counter-Strike_2/Dedicated_Servers.
        - CS2_MAPGROUP=mg_active                      # Map pool.
        - CS2_STARTMAP=de_inferno                     # Start map.
        - CS2_BOT_DIFFICULTY=                         # 0 - easy, 1 - normal, 2 - hard, 3 - expert.
        - CS2_BOT_QUOTA=6                             # Number of bots.
        - CS2_BOT_QUOTA_MODE=                         # Fill/competitive.
        - TV_AUTORECORD=0                             # Automatically records all games as CSTV demos. (0=off, 1=on)
        - TV_ENABLE=0                                 # Activates CSTV on server. (0=off, 1=on)
        - TV_PW=                                      # HCSTV password for clients.
        - TV_RELAY_PW=                                # CSTV password for relay proxies.
        - TV_MAXRATE=0                                # World snapshots to broadcast per second. Affects camera tickrate.
        - TV_DELAY=0                                  # CSTV broadcast delay in seconds.
        - CS2_LOG=on                                  # 'on','off'.
        - CS2_LOG_MONEY=0                             # Turns money logging on/off. (0=off, 1=on)
        - CS2_LOG_DETAIL=0                            # Combat damage logging. (0=disabled, 1=enemy, 2=friendly, 3=all)
        - CS2_LOG_ITEMS=0                             # Turns item logging on/off. (0=off, 1=on)
        volumes:
        - /root/peon/servers/cs2/cliffstone/actions:/actions
        - /root/peon/servers/cs2/cliffstone/data:/home/steam/steamcmd/data
        - /root/peon/servers/cs2/cliffstone/config:/home/steam/config
        user: 1000:1000
```
