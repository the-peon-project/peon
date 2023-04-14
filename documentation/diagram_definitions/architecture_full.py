from diagrams import Cluster, Diagram, Edge
from diagrams.onprem.database import Postgresql
from diagrams.onprem.container import Docker
from diagrams.onprem.client import User, Client
from diagrams.saas.chat import Discord
from diagrams.oci.compute import OKE
#from diagrams.custom import Custom

# COLOURS
comms_http = "orange"
comms_container_service = "red"
comms_container = "darkgray"

with Diagram("Peon Orchestrator Flow", filename="../documentation/manual/docs/development/architecture_master", show=False):
    # Nodes
    user = User("User")
    client_rest = Client("REST Client")
    
    client_discord = Discord("Discord")
    client_web = Client("PEON Website")
    # Clusters
    with Cluster("Container Host"):
        # Cluster - Nodes
        server = OKE("Container Service")
        container_orc = Docker("PEON Orchestrator")
        servers = [
            Docker("Game Server N"), 
            Docker("Game Server 02"), 
            Docker("Game Server 01") ]
        # Cluster - Connectivity
        container_orc >> Edge(label="docker.sock",color=comms_container_service) << server
        server - Edge(color=comms_container, style="dotted") - servers
        
    with Cluster("Management Container Host"):
        peon_web = Docker("PEON WebApp*")
        peon_web >> Edge(color=comms_http) << container_orc
        peon_bot_discord = Docker("PEON Discord Bot*")
        peon_bot_discord >> Edge(color=comms_http) << container_orc
    
    client_rest >> Edge(color=comms_http) << container_orc # DIRECT TO ORCHESTRATOR
    client_web - peon_web
    client_discord - peon_bot_discord

    user >> [client_rest, client_discord, client_web]