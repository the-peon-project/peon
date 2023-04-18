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
