# Introduction

## Architecture

This diagram shows off the basic architecture of the PEON project.

*At it's core, everything revolves around the Orcs.*

![diagram_comms](./architecture_master.png)

- REST API - The orchestrator can be managed by a REST API. The connections shown in GREEN are indicate REST communications.
- DOCKER SOCKET - The orchestrator manages the underlying docker host using docer sockets (at the moment). The connections shown in ORANGE are indicate SOCKET communications.

## Terms & Symbols

### Terms & Acronyms

| Term/Acronym | Definition |
|-|-|
| Orc | The orchestration component of the PEON project. |
| War Table | The PEON component responsible for shared services around the game servers. |
| War Plan | These are the game recipies. |
| WebUI | A website client built for the sole purpose of managing instances of *orcs* |

### Symbols

Below are the symbols that are typically found throughout the various change logs and thier meanings.

| Key | Symbol | Description |
|-|-|-|
| RELEASE | :zap: `:zap:` | When a release contains changes that impact multiple codebases in the project. :zap: **IMPACT RELEASE** :zap:|
| INITIALISED | :airplane: `:airplane:` | When the project is initialised/added to the repoisotory |
| ADDED | :new: `:new:` | When a feature/new tool/ service has been added to the codebase |
| CHANGED | :tools: `:tools:` | When a modification to the exisiting codebase/architecture has been carried out |
| OPTIMISED | :alarm_clock: `:alarm_clock:` | When a portion of the codebase has been improved visually or with regards to performance |
| REMOVED | :scissors: `:scissors:` | When something is removed/cut from the codebase |
| BUGFIX | :beetle: `:beetle:` | When a bug has been identified and resolved |
| LOGGING| :speech_balloon: `:speech_balloon:` | When logging is added/enhanced/improved |
| TESTED | :pencil: `:pencil:` | When a test task is planned & executed |
| SECURITY | :unlock: `:unlock:` | When some security modifications have been added |
