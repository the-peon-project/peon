#!/bin/bash
peon_connect_container() {
    draw_menu_header $menu_size "$app_name" "P E O N   C O N N E C T"
    PS3="Please select a container to enter: "
    container_list=$(docker ps --format "{{.Names}}" | grep -i 'peon' | grep -v 'warcamp')
    select container in $container_list; do
        case $REPLY in
        [1-${#container_list[@]}])
            echo -e "Connecting to peon infrastructure container ${BLUE}$container${STD}"
            docker exec -it $container bash
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
    pause
}

peon_restart_containers() {
    draw_menu_header $menu_size "$app_name" "P E O N   R E S T A R T"
    echo -e "[${RED}Stopping${STD}] peon infrastructure containers"
    docker-compose stop
    echo -e "[${GREEN}Starting${STD}] peon infrastructure containers"
    docker-compose up -d
    pause
}

peon_stop_containers() {
    draw_menu_header $menu_size "$app_name" "P E O N   S T O P"
    echo -e "[${RED}Stopping${STD}] peon infrastructure containers"
    docker-compose stop
    pause
}

peon_update_containers() {
    draw_menu_header $menu_size "$app_name" "P E O N   U P D A T E"
    echo -e " ${ORANGE}* NOT IMPLEMETNED YET *${STD}"
    pause
}

menu_peon() {
    local incomplete=true
    local choice
    while $incomplete; do
        draw_menu_header $menu_size "$app_name" "P E O N   C O N T A I N E R S"
        printf " 1. Connect to Container\n"
        printf " 2. Start Containers\n"
        printf " 3. Restart Containers\n"
        printf " 4. Stop Containers\n"
        printf " 5. Update Containers\n"
        printf " 0. Main Menu\n\n"
        read -p "Enter selection: " choice
        case $choice in
        0) incomplete=false ;;
        1) peon_connect_container ;;
        2) peon_start_containers ;;
        3) peon_restart_containers ;;
        4) peon_stop_containers ;;
        5) peon_update_containers ;;
        *) printf "\n ${RED_HL}*Invalid Option*${STD}\n" && sleep 0.75 ;;
        esac
    done
}
