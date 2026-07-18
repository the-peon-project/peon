# War Table

The **War Table** module works in conjunction with the Orchestrator to provide the relevant tools for the game containers.

This project handles the tools that are shared between game containers.

## Projects

[*Contained Steam*](https://github.com/the-peon-project/peon-wartable/tree/master/containers/steamcmd) (steamcmd) are scripts to automate/update `steamcmd` and the game server files (within a `steamcmd`-based docker container), as part of the PEON automation services.

[*Steamed Wine*](https://github.com/the-peon-project/peon-wartable/tree/master/containers/steamcmd-wine) (steamcmd+winhq) is a custom container to facilitate game servers that are only built for Windows OS, within the PEON tool suite.

### Modes

Modes are just unique names that help the recipe inform the server which mechanism must be followed with the automation of services. *Hopefully, this will stay a short-list*

| Mode | Release Notes | Container Tag |
| - | - | - |
| `steamcmd` | [Contained Steam](http://docs.warcamp.org/development/02_wartable/#contained-steam) | [umlatt/steamcmd](https://hub.docker.com/r/umlatt/steamcmd) |
| `steamwine` | [Steamed Wine](http://docs.warcamp.org/development/02_wartable/#steamed-wine) | [umlatt/steamcmd-winehq](https://hub.docker.com/r/umlatt/steamcmd-winehq) |
| `steamproton`  | [Steamed Proton](http://docs.warcamp.org/development/02_wartable/#steamed-proton) | [umlatt/steamcmd-proton](https://hub.docker.com/r/umlatt/steamcmd-proton) |

---

## Design Objectives

1. Only scripts/code are to be stored here. Large file pulls should be done from other sources.
2. Attempt to keep the code pool as generic as possible to maximize code reuse/supportability.
3. If something already exists and is open source, do not rewrite it needlessly.

---

## Software Stack Diagram

*\*This may change as technologies & skills evolve.*

![Software Stack](../images/diagrams/diagram_wartable.png)

---

## Navigation

Links to various project-related resources.

[![GitHub](../images/buttons/button_github.svg)](https://github.com/the-peon-project/peon-wartable)
[![GitHub](../images/buttons/button_bug.svg)](https://github.com/the-peon-project/peon-wartable/issues/new/choose)
[![GitHub](../images/buttons/button_changelog.svg)](../development/02_wartable.md#release-notes)

---

## Roadmap

Here you can see what the future holds.

- [ ] ADDED :new: `steamcmd` non-anonymous user login with steamapp authenticator flow

---

## Release Notes

---

### Contained Steam

A PEON implementation of vanilla `SteamCMD`.

**1.2.17**

- [x] BUGFIX :beetle: Added a generic self-healing update flow that retries once after backing up and clearing stale `steamapps` metadata (`appmanifest_<steam_id>.acf`, `downloading`, `temp`).

**1.2.16**

- [x] BUGFIX :beetle: Added a work around for a broken steam download cache to force a re-validate on update mode.

**1.2.15**

- [x] CHANGE :tools: Built against latest code release

**1.2.14**

- [x] CHANGE :tools: Built against latest code release

**1.2.13**

- [x] CHANGE :tools: Build version removed, responsibility given to Orc.

**1.2.12**

- [x] ADDED :new: Build version to API response
- [x] CHANGE :tools: Made public IP detection dynamic

**1.2.10**

- [x] CHANGE :tools: Updated to latest OS/package combinations.

**1.2.9**

- [x] CHANGE :tools: Updated to latest OS/package combinations.

**1.2.8**

- [x] CHANGED :tools: Fixed `.initialized` flag.

**1.2.7**

- [x] ADDED :new: Added environment variable `LOG_PATH` for redirecting outputs to the docker log

**1.2.6**

- [x] CHANGED :tools: Rebuilt off of the latest available source image.

**1.2.5**

- [x] CHANGED :tools: Rebuilt off of the latest available source image.

**1.2.4**

- [x] CHANGED :tools: Added error details as a parameter into `/`init/shared`

**1.2.1**

- [x] CHANGED :tools: Updated to the latest version of `steamcmd`

**1.2.0**

**:zap: IMPACT RELEASE :zap:**

- [x] CHANGED :tools: Reworked the container image to use less ambiguous mount options for files.
- [x] ADDED :new: Additional outputs to state file
- [x] ADDED :new: Fail on missing `/actions` folder (not being mounted)

**1.1.4**

- [x] CHANGED :tools: Maintenance release. Rebuilt image to latest base software release.

**1.1.3**

- [x] CHANGED :tools: Changed environment variable `STEAMID` to `STEAM_ID` to match builder.

**1.1.2**

- [x] ADDED :new: Set server state to `OFFLINE` on shutdown (SIGTERM sent to PID 1)
- [x] LOGGING :speech_balloon: changed the step header prefix to `[*]`

**1.1.1**

- [x] LOGGING :speech_balloon: changed the step header prefix to `[o]`
- [x] BUGFIX :beetle: fixed a permissions issue on boot.

**1.1.0**

**:zap: IMPACT RELEASE :zap:**

- [x] CHANGED :tools: reworked the entire deployment flow for better permissions and deeper PEON integration
- [x] CHANGED :tools: PEON-specific files now live in `/home/steam/peon` and do not need multiple volume mounts.
- [x] ADDED :new: A container env var that links (if exists) the relevant save data to the `/home/steam/peon/download` directory.

**1.0.6**

- [x] CHANGED :tools: Set init scripts to run as root. Only the `server_start` script is run as `steam` user.
- [x] ADDED :new: Login banner

**1.0.5**

- [x] CHANGED :tools: Set default server save path to `/home/steam/data` to match most recipes.

**1.0.3**

- [x] ADDED :new: Made `server_start` script generic (interpreter directive such as #!/bin/bash = bash script, etc.)
- [x] CHANGED :tools: Reworked the naming to allow for generic container use.

**1.0.2**

- [x] ADDED :new: Init scripts to ensure the server is updated to the latest build on boot.

**1.0.0**

- [x] INITIALISED :airplane: Initial commit

---

### Steamed Wine

A PEON implementation of vanilla `SteamCMD` with a `WINEHQ` implementation to support Windows native servers.

**1.2.17**

- [x] BUGFIX :beetle: Added a generic self-healing update flow that retries once after backing up and clearing stale `steamapps` metadata (`appmanifest_<steam_id>.acf`, `downloading`, `temp`).

**1.2.16**

- [x] BUGFIX :beetle: Added a work around for a broken steam download cache to force a re-validate on update mode.

**1.2.15**

- [x] CHANGE :tools: Built against latest code release

**1.2.14**

- [x] CHANGE :tools: Built against latest code release

**1.2.13**

- [x] CHANGE :tools: Build version removed, responsibility given to Orc.

**1.2.12**

- [x] ADDED :new: Build version to API response
- [x] CHANGE :tools: Made public IP detection dynamic

**1.2.10**

- [x] CHANGE :tools: Updated to latest OS/package combinations.

**1.2.9**

- [x] CHANGE :tools: Updated to latest OS/package combinations.

**1.2.8**

- [x] CHANGED :tools: Fixed `.initialized` flag.

**1.2.7**

- [x] ADDED :new: Added environment variable `LOG_PATH` for redirecting outputs to the docker log

**1.2.6**

- [x] CHANGED :tools: Rebuilt off of the latest available source image.

**1.2.5**

- [x] CHANGED :tools: Rebuilt off of the latest available source image.
- [x] ADDED :new: Packages `lib32gcc1-s1` and `libstdc++6` which should further enhance 32-bit application support.

**1.2.4**

- [x] CHANGED :tools: Added error details as a parameter into `/`init/shared`

**1.2.1**

- [x] CHANGED :tools: Updated to the latest version of `steamcmd`

**1.2.0**

**:zap: IMPACT RELEASE :zap:**

- [x] CHANGED :tools: Reworked the container image to use less ambiguous mount options for files.
- [x] ADDED :new: Additional outputs to state file
- [x] ADDED :new: Fail on missing `/actions` folder (not being mounted)

**1.1.4**

- [x] CHANGED :tools: Maintenance release. Rebuilt image to latest base software release.

**1.1.3**

- [x] CHANGED :tools: Changed environment variable `STEAMID` to `STEAM_ID` to match builder.

**1.1.2**

- [x] ADDED :new: Set server state to `OFFLINE` on shutdown (SIGTERM sent to PID 1)
- [x] LOGGING :speech_balloon: changed the step header prefix to `[*]`

**1.1.1**

- [x] LOGGING :speech_balloon: changed the step header prefix to `[o]`
- [x] BUGFIX :beetle: fixed a permissions issue on boot.

**1.1.0**

- [ ] ADDED :new: Add init scripts to mirror changes to PEON

**1.0.0**

- [x] ADDED :new: WINE deployed
- [x] TESTED :pencil: WINE with VRising server.
- [x] INITIALISED :airplane: Initial commit

### Steamed Proton

A PEON implementation of vanilla `SteamCMD` with the Proton layer added to more closely mirror steams emulation layers.

**1.2.17**

- [x] BUGFIX :beetle: Added a generic self-healing update flow that retries once after backing up and clearing stale `steamapps` metadata (`appmanifest_<steam_id>.acf`, `downloading`, `temp`).

**1.2.16**

- [x] BUGFIX :beetle: Added a work around for a broken steam download cache to force a re-validate on update mode.

**1.2.15**

- [x] CHANGE :tools: Change the version number to be in sync with the other steamcmd based builds
- [x] CHANGE :tools: Built against latest code release (GE's proton 10.32)

**1.0.5**

- [x] CHANGE :tools: Updated latest version of the Proton 10.12

**1.0.4**

- [x] BUGFIX :beetle: Fixed a hard coded pathing issue for the Proton tools

**1.0.3**

- [x] CHANGE :tools: Updated latest version of the Proton 10.4

**1.0.2**

- [x] CHANGE :tools: Build version removed, responsibility given to Orc.

**1.0.1**

- [x] ADDED :new: Build version to API response
- [x] CHANGE :tools: Made public IP detection dynamic

**1.0.0**

- [x] ADDED :new: Proton+WINE deployed
- [x] TESTED :pencil: Proton with Enshrouded server.
- [x] INITIALISED :airplane: Initial commit
