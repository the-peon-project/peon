from diagrams import Cluster, Diagram, Edge
from diagrams.programming.language import Python
from diagrams.onprem.container import Docker
from diagrams.saas.chat import Discord
from diagrams.generic.os import Debian
from diagrams.custom import Custom

# COLOURS
comms_http = "orange"
comms_container_service = "red"
comms_container = "darkgray"

with Diagram("Peon Discord Bot Software Stack", show=False):
    with Cluster("Container"):
        Docker("umlatt/peon.bot.discord")
        with Cluster("Application"):
            framework = Python("discord.py")
            application = Python("Peon Codebase")
            module = Python("requests")
            with Cluster("Base Image"):
                os = Debian("python:3.11-slim-bullseye")
            framework - Edge(color=comms_container, style="dotted") - application
            application - Edge(color=comms_container, style="dotted") - module
    endpoint = Discord("Discord")
    endpoint >> Edge(color=comms_http) << framework
    target = Custom("PEON Orchestrator", "./logos/peon.png")
    module >> Edge(color=comms_http) << target
    


