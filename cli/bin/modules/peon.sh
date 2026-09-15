#!/bin/bash

peon_check_orc() {
    # Checks of the orc container has been authorised to communicate to docker host
    if [[ $(docker ps | grep 'peon.orc') ]]; then
        docker exec peon.orc ls /var/run/docker.sock >/dev/null 2>&1 \
            && echo " [${BLUE}authorised${STD}]" \
            || echo " [${ORANGE}not authorised${STD}] *Please ensure that the docker services on the host are correctly mapped to the orc."
    fi
}

peon_check_health() {
    # ToDo - Centre align
    for container in $(docker ps -a --format "{{.Names}}" | grep -i 'peon' | grep -v 'warcamp'); do
        orc_state=""
        container_state=$(docker container inspect -f '{{.State.Status}}' $container)
        case $container_state in
        "created") STATE=$BLUE ;;
        "running") STATE=$GREEN ;;
        "paused") STATE=$ORANGE ;;
        "restarting") STATE=$ORANGE ;;
        "dead") STATE=$RED_HL ;;
        "exited") STATE=$RED ;;
        *) STATE=$ORANGE ;;
        esac
        if [[ "$container" == "peon.orc" ]]; then
            orc_state="$(peon_check_orc)"
        fi
        printf " $container [${STATE}$container_state${STD}]$orc_state\n"
    done
    printf "\n"
}

peon_connect_container() {
    draw_menu_header $menu_size "$app_name" "P E O N   C O N N E C T"
    PS3="Please select a container to enter: "
    container_list=$(docker ps --format "{{.Names}}" | grep -i 'peon' | grep -v 'warcamp')
    container_count=$(echo $container_list | wc -w)
    select container in $container_list; do
        case $REPLY in
        [1-$container_count])
            echo -e "Connecting to peon infrastructure container ${BLUE}$container${STD}"
            docker exec -it $container bash
            break
            ;;
        0) break ;;
        *) printf "\n ${RED_HL}*Invalid Option*${STD}\n" && sleep 0.75 ;;
        esac
    done
}

peon_get_metrics() {
    draw_menu_header $menu_size "$app_name" "P E O N   S T A T I S T I C S"
    PS3="Please select a container to view: "
    container_list=$(docker ps --format "{{.Names}}" | grep -i 'peon' | grep -v 'warcamp')
    container_count=$(echo $container_list | wc -w)
    select container in $container_list; do
        case $REPLY in
        [1-$container_count])
            echo -e "Getting peon infrastructure container ${BLUE}$container${STD} statistics"
            docker stats $container
            break
            ;;
        0) break ;;
        *) printf "\n ${RED_HL}*Invalid Option*${STD}\n" && sleep 0.75 ;;
        esac
    done
}

peon_start_containers() {
    draw_menu_header $menu_size "$app_name" "P E O N   S T A R T"
    echo -e "[${GREEN}Starting${STD}] peon infrastructure containers"
    docker-compose up -d
}

peon_restart_containers() {
    draw_menu_header $menu_size "$app_name" "P E O N   R E S T A R T"
    echo -e "[${RED}Stopping${STD}] peon infrastructure containers"
    docker-compose stop
    echo -e "[${GREEN}Starting${STD}] peon infrastructure containers"
    docker-compose up -d
}

peon_stop_containers() {
    draw_menu_header $menu_size "$app_name" "P E O N   S T O P"
    echo -e "[${RED}Stopping${STD}] peon infrastructure containers"
    docker-compose stop
}

peon_update_containers() {
    draw_menu_header $menu_size "$app_name" "P E O N   U P D A T E"
    echo -e "[${BLUE}Pulling${STD}] pull latest PEON containers"
    docker-compose pull
    echo -e "[${GREEN}Deploying${STD}] deploy the updated containers"
    docker-compose up -d
    sleep 1 # To allow reading of process
}

peon_redploy_containers() {
    draw_menu_header $menu_size "$app_name" "P E O N   R E D P L O Y"
    echo -e "[${RED}Removing${STD}] existing infrastructure containers"
    docker-compose stop
    docker-compose down --remove-orphans --volumes
    echo -e "[${BLUE}Pulling${STD}] latest version of docker-compose. TODO"
    echo -e "[${GREEN}Deploying${STD}] latest peon containers"
    docker-compose up -d
    sleep 1 # To allow reading of process
}

menu_peon() {
    cd $rootpath
    local incomplete=true
    local choice
    while $incomplete; do
        draw_menu_header $menu_size "$app_name" "P E O N   C O N T A I N E R S"
        peon_check_health
        printf " 1. Connect to Container\n"
        printf " 2. Start Containers\n"
        printf " 3. Restart Containers\n"
        printf " 4. Stop Containers\n"
        printf " 5. Update Containers\n"
        printf " 6. Redeploy containers\n"
        printf " 7. Performance Metrics\n"
        printf " 0. Main Menu\n\n"
        read -p "Enter selection: " -t 5 choice
        case $choice in
        "") pass ;;
        0) incomplete=false ;;
        1) peon_connect_container ;;
        2) peon_start_containers ;;
        3) peon_restart_containers ;;
        4) peon_stop_containers ;;
        5) peon_update_containers ;;
        6) peon_redploy_containers ;;
        7) peon_get_metrics ;;
        *) printf "\n ${RED_HL}*Invalid Option*${STD}\n" && sleep 0.75 ;;
        esac
    done
}
