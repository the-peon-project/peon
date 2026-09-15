#!/bin/bash

game_get_metrics() {
    echo -e "Getting game server container ${BLUE}$container${STD} statistics"
    docker stats $1
}

game_connect_container() {
    echo -e "Connecting to ${BLUE}$1${STD}"
        read -p " Root user? y/[n] " -t 5 choice
    if [[ "${choice,,}" == "y" ]]; then 
        docker exec -it -u root $1 bash
    else
        docker exec -it $1 bash
    fi
}

game_start_container() {
    echo -e "[${GREEN}Starting${STD}] $1"
    docker-compose up -d
    sleep 0.75
    pause
}

game_restart_container() {
    echo -e "[${RED}Stopping${STD}] $1"
    docker-compose stop
    echo -e "[${GREEN}Starting${STD}] $1"
    docker-compose up -d
    sleep 0.75
}

game_stop_container() {
    echo -e "[${RED}Stopping${STD}] $1"
    docker-compose stop
    sleep 0.75
}

game_delete_container() {
    read -p "Are you sure you want to delete the game server? y/[n] " -t 5 choice
    if [[ "${choice,,}" == "y" ]]; then 
        echo -e "[${RED_HL}Deleting${STD}] $1"
        docker-compose down
        read -p "Delete all persistent server content & config files? y/[n] " -t 5 choice
        if [[ "${choice,,}" == "y" ]]; then 
            echo "Files are being removed."
            rm -rf $2
        fi
    fi
    sleep 0.75
}

container_logs() {
    docker logs "$1"
    pause
}

game_action() {
    container=$1
    local action_incomplete=true
    local choice
    while $action_incomplete; do
        draw_menu_header $menu_size "$app_name" "G A M E  S E R V E R  A C T I O N S"
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
        printf "\n$(centre_align_to_menu $menu_size $container)\n"
        printf "${STATE}$(centre_align_to_menu $menu_size $container_state)${STD}\n\n"
        printf " 1. Connect to Container\n"
        printf " 2. Start Container\n"
        printf " 3. Restart Container\n"
        printf " 4. Stop Container\n"
        printf " 5. Logs\n"
        printf " 6. Server Metrics\n"
        printf " 8. Delete Container\n"
        printf " 0. Back\n\n"
        read -p "Enter selection: " -t 5 choice
        server_path=$(echo "$rootpath/servers/$container" | sed "s/peon.warcamp.//g" | sed "s/\./\//g")
        cd $server_path
        case $choice in
        "") pass ;;
        0) action_incomplete=false ;;
        1) game_connect_container $container;;
        2) game_start_container $container;;
        3) game_restart_container $container;;
        4) game_stop_container $container;;
        5) container_logs $container;;
        6) game_get_metrics $container;;
        8) game_delete_container $container; break ;;
        *) printf "\n ${RED_HL}*Invalid Option*${STD}\n" && sleep 0.75 ;;
        esac
    done
}

menu_game() {
    local game_incomplete=true
    local choice
    while $game_incomplete; do
        draw_menu_header $menu_size "$app_name" "G A M E   C O N T A I N E R S"
        PS3="Enter selection: "
        container_list=$(docker ps -a --format "{{.Names}}" | grep -i 'peon.warcamp' | sort)
        container_count=$(echo $container_list | wc -w)
        if [ "$container_count" -gt "0" ]; then
            select container in $container_list; do
                case $REPLY in
                [1-$container_count])
                    game_action $container
                    break
                    ;;
                0)
                    game_incomplete=false
                    break
                    ;;
                *) printf "\n ${RED_HL}*Invalid Option*${STD}\n" && sleep 0.75 ;;
                esac
            done
        else
            printf "\nThere are currently no game servers on this host.\n\n"
            read -p "Press enter to continue."
            game_incomplete=false
        fi
    done
}
