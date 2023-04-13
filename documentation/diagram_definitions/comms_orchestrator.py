from diagrams import Cluster, Diagram, Edge
from diagrams.onprem.database import Postgresql
from diagrams.onprem.container import Docker
from diagrams.onprem.client import User, Client
from diagrams.saas.chat import Discord
from diagrams.oci.compute import OKE
from diagrams.custom import Custom

comms_http = "darkgreen"
comms_container_service = "darkblue"
comms_container = "darkblue"

with Diagram("Peon Orchestrator Flow", filename="../documentation/manual/docs/architecture/comms_orchestrator", show=False):
    # Nodes
    user = User("User")
    client_rest = Client("REST Client")
    peon_web = Docker("PEON WebApp*")
    bot_discord = Docker("PEON Discord Bot*")
    client_discord = Discord("Discord")
    client_web = Client("WebUI Portal")
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
    # Connectivity
    client_rest >> Edge(color=comms_http) << container_orc
    # Web
    client_web - peon_web
    peon_web >> Edge(color=comms_http) << container_orc
    # Discord
    client_discord - bot_discord
    bot_discord >> Edge(color=comms_http) << container_orc
    # User
    user >> [client_rest, client_discord, client_web]