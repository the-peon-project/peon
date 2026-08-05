# Introduction

Here are the notes on the game server development.

## Resources

### Dedicated Server Possibilities

#### Steam

An active development list can be found [here](https://developer.valvesoftware.com/wiki/Dedicated_Servers_List)

## Development Guidelines

### Standardization

The aim is to figure out how to standardize the deployment of servers such that creating and deploying new servers is as simple as possible.

#### Hierarchy of importance

When a technical decision needs to be made, the below list indicates how the outcome should be decided best. *For example_, if a particular architecture is easy_ to implement, but at the cost of user functionality, then try to identify a better solution.*

- User simplicity: The overriding deciding factor will always be, what would make the experience better for the user.
- Developer Simplicity: The second highest priority is making extending the platform's functionality should be paramount to the design decision.
- Default Builds: If possible, default to the `umlatt/steamcmd`/`umlatt/steamcmd-wine`-based container image/s that have been built with PEON in mind. This should reduce the need for custom work for the rest of the platform. *Even if that means opening up a ticket against the relevant project so that we can improve it accordingly.

> *Don't be afraid to discard excellent code, just because its excellent. Good code can always find another home. A poor use of good code is a poor use of time.*

### Untested rollout status

The game catalog now uses explicit rollout stages (`working`, `untested`, `planned`).

- Product-facing list: [Supported Games](../../games.md)
- Engineering expectation: each `untested` title needs dedicated-server app-id verification, startup command validation, and game-specific port/storage hardening before promotion to `working`.
- Product docs intentionally list only self-hostable servers.

### Directory Structure

```bash
./data/             # DIR: This is where the game server binaries/files are stored
./peon/             # DIR: This is for PEON status information files
./upload/           # DIR: *This is a folder where custom settings files can be uploaded so that they can be implemented.
./user/             # DIR: *This should be mapped to any user data that needs to be retained (such as a 'world save')
.env                # FILE: This is the main configuration mechanism. All customizations should be implemented here.
docker-compose.yml  # FILE: This defines the game server build. No hard coding of settings is to be done here (unless they are unchangeable)
settings.json       # FILE: *This file will be the main mechanism the orchestrator will use to understand the mapping of the server to the host. (Such as custom/changeable files and so on) 
sever_start         # FILE: This file defines which command and how to run it, in order for the unique server instance to start.
```

*\*These are not always used.*

### Settings File

:warning: The `settings.json` file is required for all recipes (when being used by PEON) as it provides the relevant directive to PEON, to handle the container appropriately.

#### metadata

The information about the plan as well as indicating to PEON which deployment paradigm must be followed

| Key | Example | Description |
| - | - | - |
| `gid` | `csgo` | the **PEON** game id (this value is what PEON uses to manage the appropriate game resources) |
| `version` | `1.0.1` | The current PEON build based on the release notes |
| `mode` | `steamcmd` | Informs the Orchestrator which container and therefore paradigm must be used to handle the resource. The only mode possibilities are defined by what is supported by PEON currently. [WarTable/Modes](http://docs.warcamp.org/development/02_wartable/#modes)|

#### env_vars

These are environment variables that are supplied to the relevant container. (They are pushed into the `.env` file for the server)

The environment variable name is provided as a key, with its value being a collection of settings.

Each environment variable is made up of three component settings.

| Key |  Description |
| - | - |
| `default` |  This is the default setting, as defined by the plan (and will not be changed) |
| `value` |  This is the new setting (it will override what is in default within the container)s |
| `optional` | This indicates whether or not this value is required by the plan. |

*If there are no special `env_vars` to provide, you may leave this section out.*

#### files

These are for locating the game server's specific config files. This should allow fine-grained control over the server's functioning for more advanced users.

The key, in files, is the filename, with the values containing file metadata.

| Key |  Description |
| - | - |
| `path` |  This indicates the path, within the container, where the file should/does reside. |
| `sample` |  This indicates that there is a default file in that location (which can then be retrieved for the user to configure) |
| `default` | This indicates to PEON whether the server is running a user-modified file or the default file. |

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
