#!/bin/bash
#
# S E C U R I T Y
#
# Create ssh key in orchestrator
docker exec -it peon.orc ssh-keygen -b 2048 -t rsa -f /root/.ssh/id_rsa -q -N ""
# Update authorized keys on docker host
docker exec -it peon.orc cat /root/.ssh/id_rsa.pub >> /root/.ssh/authorized_keys