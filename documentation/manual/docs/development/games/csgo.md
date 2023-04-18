# CSGO

The PEON war plan that Peon uses to deploy your game server.

![CS:GO](../../logos/csgo.png)

## Official Documentation

[Original Guide](https://developer.valvesoftware.com/wiki/Counter-Strike:_Global_Offensive_Dedicated_Servers#Docker)

- If you wish to change the default server settings, log in to the host that is running the server, navigate to `./peon/servers/csgo/*servername*/`. You can edit the `server_start` file to configure the flags.
- Alternatively, you should be able to edit the server files in the data directory of the server (e.g. ``./peon/servers/[game_uid]/[server_name]/``)
- Logging can be seen by running `docker ps` to get a list of running servers, then `docker logs --follow [CSGO:Server container name/ID]`

### Game Server Login Token (GSLT)

CSGO required a `GSLT` to run on thier public network

### Code Repo

- [Github Project](https://github.com/the-peon-project/peon-warplans/tree/main/csgo)
