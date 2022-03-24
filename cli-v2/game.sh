#!/bin/bash

game_connect_container(){
    echo -e "Connecting to ${BLUE}$container${STD}"
    docker exec -it $1 bash
}

game_start_container(){
    echo -e "[${GREEN}Starting${STD}] $1"
    docker start $1
    sleep 0.75
}

game_restart_container(){
    echo -e "[${RED}Stopping${STD}] $1"
    docker stop $1
    echo -e "[${GREEN}Starting${STD}] $1"
    docker start $1
    sleep 0.75
}

game_stop_container(){
    echo -e "[${RED}Stopping${STD}] $1"
    docker stop $1
    sleep 0.75
}

game_action(){
    container=$1
    local action_incomplete=true
    local choice
    while $action_incomplete; do
        draw_menu_header $menu_size "$app_name" "G A M E  S E R V E R  A C T I O N S"
        case $(docker container inspect -f '{{.State.Status}}' $container) in
            "running") STATE=$GREEN ;;
            *) STATE=$ORANGE;;
        esac
        printf "\n *${STATE} $container ${STD}*\n"
        printf " 1. Connect to Container\n"
        printf " 2. Start Container\n"
        printf " 3. Restart Container\n"
        printf " 4. Stop Container\n"
        printf " 0. Back\n\n"
        read -p "Enter selection: " choice
        case $choice in
            0) action_incomplete=false;;
            1) game_connect_container $container;;
            2) game_start_container $container;;
            3) game_restart_container $container;;
            4) game_stop_container $container;;
            *) printf "\n ${RED_HL}*Invalid Option*${STD}\n" && sleep 0.75 ;;
        esac
    done
}

menu_game (){
    local game_incomplete=true
    local choice
    while $game_incomplete; do
        draw_menu_header $menu_size "$app_name" "G A M E   C O N T A I N E R S"
        PS3="Select a game container to manage: "
        container_list=$(docker ps -a --format "{{.Names}}" | grep -i 'peon.warcamp')
        select container in $container_list; do
            case $REPLY in
            [1-${#container_list[@]}]) game_action $container; break;;
            0) game_incomplete=false; break ;;
            *) printf "\n ${RED_HL}*Invalid Option*${STD}\n" && sleep 0.75 ;;
            esac
        done
    done
}