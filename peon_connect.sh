#!/bin/bash
PS3="Please select a container to enter: "
container_list=`docker ps --format "{{.Names}}" | grep -i 'peon'`
select container in $container_list; do
    if [ $REPLY -gt 0 ]; then
        echo -e "Connecting to [\033[0;32m$container\033[0m]"
        docker exec -it $container bash
    else
        echo "Invalid selection. Exiting..."
    fi
    exit 0
done