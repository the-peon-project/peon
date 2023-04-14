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
    with Cluster("Docker Hub"):
        image_n = Docker("Image.N")
        image_2 = Docker("Image.2")
        image_1 = Docker("Image.1")
    runtime << [image_n,image_2,image_1]
    svc = Github("Plan Repository")
    svc << application
    endpoint = Inspection("REST API")
    endpoint >>  framework


