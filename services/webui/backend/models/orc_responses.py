"""Typed shapes for orc's (services/orc) API responses, used at the webui<->orc
boundary in routes/proxy.py so a shape drift in orc's API surfaces as a clear
validation error here instead of an unexplained KeyError deeper in the request.

Field names below were verified against services/orc/app/modules/servers.py's
server_get_server()/servers_get_all() and app/modules/plans.py's get_plans_local() --
orc's server payloads carry `game_uid` + `servername` (never a `server_uid` key on
the wire; webui/bot-discord each compute that identifier client-side as
f"{game_uid}.{servername}"), and its plan entries carry `game_uid` + `title`.
"""
from pydantic import BaseModel, ConfigDict, computed_field


class OrcServer(BaseModel):
    model_config = ConfigDict(extra="allow")  # orc's server payload has many
    # optional/variable fields (server_config, stats, description, etc.) --
    # this model only pins down the fields every consumer actually depends on.

    game_uid: str
    servername: str

    @computed_field
    @property
    def server_uid(self) -> str:
        """Convenience identifier matching what webui/bot-discord already
        compute by hand from game_uid + servername."""
        return f"{self.game_uid}.{self.servername}"


class OrcPlan(BaseModel):
    model_config = ConfigDict(extra="allow")

    game_uid: str
    title: str
