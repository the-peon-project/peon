from diagrams import Cluster, Diagram, Edge
from diagrams.programming.language import Bash
from diagrams.onprem.container import Docker
from diagrams.custom import Custom
import os

# COLOURS
comms_http = "orange"
comms_container_service = "red"
comms_container = "darkgray"

current_path = os.getcwd()


with Diagram("Peon War Plan Software Stack", filename="../manual/docs/images/diagrams/diagram_warplans", show=False):
    with Cluster("Container"):
        with Cluster("Gamer Server"):
            scripts = Bash("Scripts")
            steam = Custom("SteamCMD",f"{current_path}/diagram_definitions/logos/steam.png")
            scripts >> steam
        container = Docker("steamcmd/steamcmd")
    definition = Custom("docker-compose.yml",f"{current_path}/diagram_definitions/logos/docker-compose.png")
    conf_file = Custom(".env",f"{current_path}/diagram_definitions/logos/env.png")
    [ definition, conf_file ] - Edge(style="dotted") - scripts
    