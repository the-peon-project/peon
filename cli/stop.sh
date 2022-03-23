#!/bin/bash
echo "What would you like to stop?"
options=("Everything Peon-servers Game-server")
PS3="Select stop category: "
select category in $options; do
    if [ $REPLY -gt 0 ]; then
        case $REPLY in
        1)
            echo -e "> \033[0;31mStopping\033[0m ALL containers."
            for container in $(docker ps -q); do docker stop $container; done
            ;;
        2)
            echo -e "> \033[0;31mStopping\033[0m Peon infrastructure containers"
            docker-compose stop
            ;;
        3)
            PS3="Select a server to stop: "
            container_list=$(docker ps -a --format "{{.Names}}" | grep -i 'peon.warcamp')
            select container in $container_list; do
                if [ $REPLY -gt 0 ]; then
                    echo -e "> \033[0;31mStopping\033[0m server [$container]"
                    docker stop $container
                    exit 0
                fi
            done
            ;;
        *) echo "Invalid selection [$REPLY]. Exiting..." ;;
        esac
    else
        echo "Invalid selection. Exiting..."
    fi
    exit 0
done