# Introduction

Here are the notes on the game server development.

## Basic guidlines

### Standardization

1. Default Builds: If possible, default to the  `umlatt/steamcmd`/`umlatt/steamcmd-wine` based container image/s that have been built with PEON in mind. This should reduce the need for custom work to the rest of the platform. *Even if that means opening up a ticket against the relevant project so that we can improve it accordingly.

### Directory Structure

```bash
./server_files/     # DIR: This is where the downloaded game server files are stored
./status/           # DIR: This is for PEON status information files
./upload/           # DIR: *This is a folder where custom settings files can be uploaded, so that they can be implemented.
./download/         # DIR: *This should be mapped to any user data that needs to be retained (such as a 'world save')
.env                # FILE: This is the main configuration mechanism. All customizations should be implemented here.
docker-compose.yml  # FILE: This defines the game server build. No hard coding of settings to be done here
settings.json       # FILE: *This is file for helping to map files from './upload/ to thier correct places. (Essentially, this is how we facilitate the uploading of config files.) 
sever_start         # FILE: This file defines what command and how to run it, in order for the unique server instance to start.
```

*\*These are not always used.*

### Settings File

:warning: The `settings.json` file is required for all recipies (when being used by PEON) as it provides the relevant directive to PEON, in order to handle the container appropriately.

#### metadata

The information about the plan as well as indicating to PEON which deployment paradym must be followed

- **gid** - the PEON game id
- **version** - the current release based on the flag in release notes
- **mode** - defines which deployment paradym to use for the container

#### env_vars

These are environment variables that are supplied to the relevant container. (They are pushed into the `.env` file for the server)

The environment variable name is provided as a key, with its value being a collection of settings.

Each environment variable is made up of three component settings.

- **default** - This is the default setting, as defined by the plan (and will not be changed)
- **value** - This is the new setting (it will override what is in default within the container)
- **optional** - This indicates whether or not this value must be provided.

*If there are no special `env_vars` to provide, you may leave this section out.*

#### files

These are for locating the game server's specific config files. This should allow fine grained controll over the server's functioning for more advanced users.

The key, in files, is the filename, with the values containing file metadata.

- **path** - this indicates the path, within the container, where the file should/does reside.
- **sample** - this indicates that there is a default file in that location (which can then be retrieved for the user to configure)
- **default** - this indicates to PEON whether the server is running a user modified file.

*If there are no special `config_files` to provide, you may leave this section out.*

#### Example

```json
{
    "metadata" : {
        "gid" : "csgo",
        "version" : "1.0.0",
        "mode" : "steamcmd"
    },
    "env_vars" : {
        "STEAM_GSLT"     : { "default" : 0,             "value" : null, "optional" : true },
        "CSGO_GAME_TYPE" : { "default" : 0,             "value" : null, "optional" : true },
        "CSGO_GAME_MODE" : { "default" : 0,             "value" : null, "optional" : true },
        "CSGO_MAP_GROUP" : { "default" : "mg_active",   "value" : null, "optional" : true },
        "CSGO_MAP"       : { "default" : "de_dust2",    "value" : null, "optional" : true }
    },
    "files" : {
        "autoexec.cfg"          : { "path" : "/home/steam/server_files/csgo/cfg/autoexec.cfg", "sample" : null, "default" : true},
        "server.cfg"            : { "path" : "/home/steam/server_files/csgo/cfg/server.cfg", "sample" : null,  "default" : true},
        "gamemodes.txt"         : { "path" : "/home/steam/server_files/csgo/gamemodes.txt", "sample" : "/home/steam/server_files/csgo/gamemodes.txt",  "default" : true},
        "gamemodes_server.txt"  : { "path" : "/home/steam/server_files/csgo/gamemodes_server.txt", "sample" : "gamemodes_server.txt.example",  "default" : true}
    }
}
```
