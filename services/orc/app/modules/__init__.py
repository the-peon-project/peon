import json
import os
import docker

install_path = os.environ.get("PEON_INSTALL_PATH", "/app")
schedule_file="/home/peon/servers/schedule.json"

# Settings file
settings = json.load(open(f"{install_path}/config.json", 'r'))
# Container prefix
prefix = "peon.warcamp."
# Docker client file
client = docker.from_env()