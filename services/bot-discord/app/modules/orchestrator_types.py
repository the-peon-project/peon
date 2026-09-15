"""Typed shapes for orc's API responses, mirroring
services/webui/backend/models/orc_responses.py's OrcServer/OrcPlan -- kept as a
separate, per-service definition rather than a shared package (see the repo's
architecture-review plan's Global Constraints on cross-service coupling).

Field names were verified against services/orc/app/modules/servers.py's
server_get_server()/servers_get_all() and app/modules/plans.py's
get_plans_local() -- orc's server payloads carry `game_uid` + `servername`
(there is no `server_uid` key on the wire; this module's own
server_actions()/get_servers_all() already compute that identifier by hand as
f"{game_uid}.{servername}"), and its plan entries carry `game_uid` + `title`.
"""
from typing import Any, TypedDict


class OrcServer(TypedDict, total=False):
    game_uid: str
    servername: str
    container_type: str
    build_version: str
    container_state: str
    server_state: str
    server_config: dict
    description: str
    time: Any


class OrcPlan(TypedDict, total=False):
    game_uid: str
    title: str
