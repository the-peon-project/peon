# REST API

All orchestrators are managed/controlled directly with the REST API.

The orchestrator now exposes FastAPI OpenAPI docs directly. In a default PEON WebUI deployment, open the Swagger viewer through the WebUI sub-path:

`/api/proxy/{orchestrator_id}/docs`

This keeps API docs inside the main dashboard surface, and removes the need for a standalone Swagger UI container in default deployments.

---

## RESTful API

We are using a RESTful API as it is quite easy and there are plenty of guides on how to use REST as a technology.

A [Postman collection file](https://github.com/the-peon-project/peon-docs/blob/main/api/v1/peon-api-v1.0-postman.json) can be used for convenience.

---

### Authorization

We plan on supporting more and more authorization methods. Currently, the below list is what is supported.

#### API-KEY

The defaults are as below. Please change these in the `.env` file for the orchestrator.

| header key | value |
| - | - |
| `X-Api-Key` | `my-super-secret-api-key` |

---

### Basic Overview

This API expects a JSON payload in *most* cases.

#### Base URI/URL

The base follows the standard below.

```bash
# structure
{{peon_orchestrator_url}}:{{api_port}}/api/v1/

# some valid examples include
https://gameserver.cloud:5000/api/v1/
http://192.168.20.2:5000/api/v1/
http://localhost:5000/api/v1/
```

We are currently on version `1.0` of the API. We will try to keep from having to change endpoints, however, if that has to happen we'll opt to create a new version.

#### Endpoints

The below endpoints are the current GA endpoints for the PEON Orchestrator

---

##### Servers

Will list all game servers that are registered to the Orchestrator.

```yaml
    servers:
        - [GET] List all servers registered to Orchestrator
        - [PUT] Scan the servers folder and import any available servers
```

###### Payload

*No payload required*

###### Example

Creating a `Valheim` server

URL

```url
http://orc.domain.com:5000/api/v1/servers
```

HEADERS

```json
{ "X-Api-Key" : "my-super-secret-api-key" }
```

PAYLOAD [BODY]

*N/A*

---

##### Server

Used for managing a specific server instance with a known `SERVERNAME`.

```yaml
    server/get/GAME_UID.SERVERNAME:
        - [GET] Get details of a game server
    server/stats/GAME_UID.SERVERNAME:
        - [GET] Get details of a game server, with performance statistics
    server/save/GAME_UID.SERVERNAME:
        - [GET] Download a copy of the config and user files for a server.
    server/create/GAME_UID.SERVERNAME:
        - [PUT] Create a new game server
        payload: { "description": "A PEON game server for ark.", "start_later" : true, "setting01" : "value01", "setting02" : "value02", "setting0N" : "value0N"} *description & start_later are optional. **All other settings can be found be querying the game servers's relevant plan.
    server/start/GAME_UID.SERVERNAME:
        - [PUT] Start a specific game server from the Orchestrator
    server/stop/GAME_UID.SERVERNAME:
        - [PUT] Stop a specific game server from the Orchestrator
    server/restart/GAME_UID.SERVERNAME:
        - [PUT] Restart a specific game server from the Orchestrator
    server/description/GAME_UID.SERVERNAME:
        - [PUT] Update the description of a specific game server from the Orchestrator
    server/destroy/GAME_UID.SERVERNAME:
        - [DEL] Removes a game container leaving the server and config files intact (optional flag to delete all files as well)
        payload: { "eradicate" : "True" } *Optional (destructive data removal)
    server/eradicate/GAME_UID.SERVERNAME:
        - [DEL] Deletes all game data & config files
        payload: { "eradicate" : "True" } *Required
```

###### Example

Creating a `Valheim` server
*Query your Orc's API for the intended game's plan for the relevant settings (e.g. `/api/v1/plan/valheim`). Settings with empty `""` are required settings. The others are optional.

URL

```url
http://orc.domain.com:5000/api/v1/server/create/{{GAME_UID}}.{{SERVERNAME}}
```

The {{GAME_UID}} value needs to be available to your Orcestrator's plan list.
The {{SERVERNAME}} value can be different from what is provided in the payload. This {{SERVERNAME}} value will form part of the game server's unique ID and will be how the server is referenced going forward.

HEADERS

```json
{ "X-Api-Key" : "my-super-secret-api-key" }
```

PAYLOAD [BODY]

Only `JSON` payloads are currently supported.

```json
{
    "SERVER_NAME": "",
    "WORLD_NAME": "",
    "PASSWORD": "",
    "description": "A PEON game server for valheim."
}
```

---

##### Plans

Manage available game plans.

```yaml
    plans:
        - [GET] List all local game plans.
    plans:
        - [PUT] Download latest game plan list from Peon Project.
```

###### Payload

*No payload required*

###### Example
Listing the locally available game plans.

URL

```url
http://orc.domain.com:5000/api/v1/plans
```

HEADERS

```json
{ "X-Api-Key" : "my-super-secret-api-key" }
```

PAYLOAD [BODY]

*N/A*

---

##### Plan

Manage a specific game plan.

```yaml
    plan/GAME_UID:
        - [GET] Get the required/optional settings for a specific game plan.
```

###### Payload

*No payload required*

###### Example
Listing the locally available game plans.

URL

```url
http://orc.domain.com:5000/api/v1/plan/{{GAME_UID}}
```

HEADERS

```json
{ "X-Api-Key" : "my-super-secret-api-key" }
```

PAYLOAD [BODY]

*N/A*

---