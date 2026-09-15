# Sons of the Forest

The PEON war plan that Peon uses to deploy a Sons of the Forest dedicated game server with minimal effort.

![Sons of the Forest](./logo.png)

## Documentation

If you would like info on how to use this plan, the up-to-date documentation can be found in the [PEON project game guide](http://docs.warcamp.org/guides/games/sof/).

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
        container_name: peon.warcamp.sof.myforest
        hostname: peon.warcamp.sof.myforest
        image: jammsen/sons-of-the-forest-dedicated-server
        ports:
        - 8766:8766/udp
        - 27016:27016/udp
        - 9700:9700/udp
        environment:
        - STEAM_ID=2465200                            # Steam app ID for Sons of the Forest.
        - SERVER_NAME=My Forest Server                # Set the visible name for your server.
        - PASSWORD=                                   # Server password (leave empty for public).
        - PASSWORD_ADMIN=changeme                     # Admin password.
        - MAX_PLAYERS=8                               # Maximum players (1-8).
        - DIFFICULTY=Normal                           # Game difficulty (Peaceful, Normal, Hard).
        - SAVE_SLOT=1                                 # Save slot (1-5).
        - SAVE_MODE=New                               # Save mode (New, Continue).
        - AUTO_SAVE_INTERVAL=30                       # Auto save interval in minutes.
        - ENABLE_VAC=true                             # Enable Valve Anti-Cheat.
        - SERVER_CONTACT=admin@example.com            # Admin contact email.
        - TREE_REGROW_MODE=false                      # Enable tree regrowth.
        - ALLOW_BUILDING_DESTRUCTION=true             # Allow building destruction.
        - ALLOW_ENEMIES_CREATIVE=false                # Allow enemies in creative mode.
        - ENABLE_ENEMIES=true                         # Enable enemy spawning.
        volumes:
        - /root/peon/servers/sof/myforest/actions:/actions
        - /root/peon/servers/sof/myforest/data:/home/steam/steamcmd/sof
        - /root/peon/servers/sof/myforest/config:/home/steam/.config/unity3d/Endnight/SonsOfTheForestDS
```
