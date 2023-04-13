from diagrams import Cluster, Diagram, Edge
from diagrams.onprem.database import Postgresql
from diagrams.onprem.container import Docker
from diagrams.onprem.client import User, Client
from diagrams.saas.chat import Discord
from diagrams.oci.compute import OKE

comms_http = "darkgreen"
comms_container_service = "darkblue"
comms_container = "darkblue"

with Diagram("Peon Orchestrator", filename="../documentation/manual/docs/architecture/comms_orchestrator", show=False):
    # Nodes
    client_user = User("User")
    client_bot_discord = Discord("Discord Bot*")
    peon_web = Client("PEON WebApp*")
    # Clusters
    with Cluster("Container Host"):
        # Cluster - Nodes
        server = OKE("Container Service")
        container_orc = Docker("Orchestrator")
        servers = [
            Docker("Game Server N"), 
            Docker("Game Server 02"), 
            Docker("Game Server 01") ]
        # Cluster - Connectivity
        container_orc >> Edge(label="docker.sock",color=comms_container_service) << server
        server - Edge(color=comms_container, style="dotted") - servers

    # Connectivity
    client_user >> Edge(label="REST API", color=comms_http) << container_orc
    client_bot_discord >> Edge(label="REST API", color=comms_http) << container_orc
    peon_web >> Edge(label="REST API", color=comms_http) << container_orc