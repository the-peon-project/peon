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


with Diagram("Peon War Table Software Stack", filename="../manual/docs/images/diagrams/diagram_wartable", show=False):
    with Cluster("Container"):
        with Cluster("Application"):
            wine = Custom("WINE",f"{current_path}/diagram_definitions/logos/wine.png")
            with Cluster("Base Image"):
                steam = Custom("SteamCMD",f"{current_path}/diagram_definitions/logos/steam.png")
        Docker("umlatt/steamcmd-winehq")
    Bash("Automation Scripts")