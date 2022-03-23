#!/bin/bash
echo "What would you like to restart?"
options=("Everything Peon-servers Game-server")
PS3="Select restart category: "
select category in $options; do
    if [ $REPLY -gt 0 ]; then
        case $REPLY in
        1)
            echo -e "> \033[0;31mStopping\033[0m ALL containers."
            for container in $(docker ps -q); do docker start $container; done
            echo -e "> \033[0;32mStarting\033[0m ALL containers."
            for container in $(docker ps -q); do docker start $container; done
            ;;
        2)
            echo -e "> \033[0;31mStopping\033[0m Peon infrastructure containers"
            docker-compose stop
            echo -e "> \033[0;32mStarting\033[0m Peon infrastructure containers"
            docker-compose up -d
            ;;
        3)
            PS3="Select a server to restart: "
            container_list=$(docker ps -a --format "{{.Names}}" | grep -i 'peon.warcamp')
            select container in $container_list; do
                if [ $REPLY -gt 0 ]; then
                    echo -e "> \033[0;31mStopping\033[0m server [$container]"
                    docker stop $container
                    echo -e "> \033[0;32mStarting\033[0m server [$container]"
                    docker start $container
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