from diagrams import Cluster, Diagram, Edge
from diagrams.programming.framework import Flask
from diagrams.programming.language import Python, Bash
from diagrams.onprem.container import Docker
from diagrams.onprem.vcs import Github
from diagrams.generic.os import Debian
from diagrams.programming.flowchart import Inspection
from diagrams.oci.compute import OKE

# COLOURS
comms_http = "orange"
comms_container_service = "red"
comms_container = "darkgray"

with Diagram("Peon Orchestrator Software Stack", filename="../documentation/manual/docs/development/diagram_orc", show=False):
    with Cluster("Docker Host"):
        runtime = OKE("Container Runtime")
        with Cluster("Container"):
            Docker("umlatt/peon.orc")
            with Cluster("Application"):
                framework = Flask()
                application = Python("Peon Codebase")
                shell = Bash("Support Scripts")
                with Cluster("Base Image"):
                    os = Debian("python:3.11")
                framework - Edge(color=comms_container, style="dotted") - application
                application - Edge(color=comms_container, style="dotted") - shell
        shell >> runtime
        application >> runtime
    svc = Github("Plan Repository")
    endpoint = Inspection("REST API")
    endpoint >>  framework
    svc << application

