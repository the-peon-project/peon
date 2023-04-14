from diagrams import Cluster, Diagram, Edge
from diagrams.programming.framework import Flask
from diagrams.programming.language import Python, Bash
from diagrams.onprem.container import Docker
from diagrams.onprem.vcs import Github
from diagrams.generic.os import Debian
from diagrams.programming.flowchart import Inspection

# COLOURS
comms_http = "orange"
comms_container_service = "red"
comms_container = "darkgray"




with Diagram("Peon Orchestrator Software Stack", filename="../documentation/manual/docs/development/orchestrator/diagram", show=False):
    with Cluster("*Container Runtime*"):
        runtime = Docker("Docker Socket")
        with Cluster("Container: umlatt/peon.orc"):
            with Cluster("Application"):
                framework = Flask()
                application = Python("Peon Application")
                shell = Bash("Support Scripts")
                with Cluster("Base Image"):
                    os = Debian("python:3.11")
                framework - Edge(color=comms_container, style="dotted") - application
                application >> shell
        shell >> runtime
        application >> runtime
    svc = Github("Plan Repository")
    endpoint = Inspection("REST API")
    endpoint >> framework
    svc >> application

