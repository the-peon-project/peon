#!/bin/bash
#
# S E C U R I T Y
#
# Create ssh key in orchestrator
docker exec -it peon.orc ssh-keygen -b 2048 -t rsa -f /root/.ssh/id_rsa -q -N ""
# Update authorized keys on docker host
docker exec -it peon.orc bash -c "cat /root/.ssh/id_rsa.pub" >> /root/.ssh/authorized_keys
# Preload ECDSA key
docker exec -it peon.orc bash -c "ssh-keyscan -p 22222 -t rsa 172.20.0.1 | sed -E 's/^([^ \[]+) (.*)$/[\1]:NNN \2/' >> ~/.ssh/known_hosts"  > /dev/null 2>&1
# Copy docker cli binary into container - MAY NOT BE BEST WAY (different OS's/builds)
docker cp /usr/bin/docker peon.orc:/usr/bin/.
