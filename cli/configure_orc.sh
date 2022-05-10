#!/bin/bash
#
# S E C U R I T Y
#
# Create ssh key in orchestrator
if docker exec -it peon.orc ls /root/.ssh/ | grep id_rsa.pub &>/dev/null; then
    echo "Public key already exists in Orchestrator"
else
    docker exec -it peon.orc ssh-keygen -b 2048 -t rsa -f /root/.ssh/id_rsa -q -N ""
fi
# Clean previous authorized keys
sed -i '/peon.orc/d' /root/.ssh/authorized_keys
if docker exec -it peon.orc ls /root/.ssh/ | grep id_rsa.pub &>/dev/null; then
    # Update authorized keys on docker host
    docker exec -it peon.orc bash -c "cat /root/.ssh/id_rsa.pub" >> /root/.ssh/authorized_keys
    # Preload ECDSA key
    docker exec -it peon.orc bash -c "ssh-keyscan -p 22222 -t rsa 172.20.0.1 | sed -E 's/^([^ \[]+) (.*)$/[\1]:NNN \2/' >> ~/.ssh/known_hosts"  > /dev/null 2>&1
fi
#
# D O C K E R    B I N A R Y
#
# Import docker hosts current binary version
docker cp $(which docker) peon.orc:/usr/bin/.
