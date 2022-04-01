#!/bin/bash

game_get_metrics() {
    echo -e "Getting game server container ${BLUE}$container${STD} statistics"
    docker stats $1
}

game_connect_container() {
    echo -e "Connecting to ${BLUE}$1${STD}"
    docker exec -it $1 bash
}

game_start_container() {
    echo -e "[${GREEN}Starting${STD}] $1"
    docker start $1
    sleep 0.75
}

game_restart_container() {
    echo -e "[${RED}Stopping${STD}] $1"
    docker stop $1
    echo -e "[${GREEN}Starting${STD}] $1"
    docker start $1
    sleep 0.75
}

game_stop_container() {
    echo -e "[${RED}Stopping${STD}] $1"
    docker stop $1
    sleep 0.75
}

game_container_logs() {
    docker logs "$1"
    pause
}

game_server_logs() {
    docker_go_data=($(docker inspect -f '{{.Mounts}}' $1))
    for chunk in "${docker_go_data[@]}"; do
        if [[ $chunk == *"/var/log/peon/"* ]]; then log_path="$chunk"; fi
    done
    log_files=($(ls $log_path))
    printf "\n━ Game Server Logs ━\n${BLUE}$log_path${STD}\n"
    select log in $(ls $log_path); do
        case $REPLY in
        [1-${#log_files[@]}])
            clear
            cat "$log_path/$log"
            read -n 1 -s result
            break
            ;;
        0)
            break
            ;;
        *) printf "\n ${RED_HL}*Invalid Option*${STD}\n" && sleep 0.75 ;;
        esac
    done
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
        printf " 5. Container logs\n"
        printf " 6. Server logs\n"
        printf " 7. Server Metrics\n"
        printf " 0. Back\n\n"
        read -p "Enter selection: " -t 5 choice
        case $choice in
        "") pass ;;
        0) action_incomplete=false ;;
        1) game_connect_container $container ;;
        2) game_start_container $container ;;
        3) game_restart_container $container ;;
        4) game_stop_container $container ;;
        5) game_container_logs $container ;;
        6) game_server_logs $container ;;
        7) game_get_metrics $container;;
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
        container_list=$(docker ps -a --format "{{.Names}}" | grep -i 'peon.warcamp')
        container_count=`echo $container_list | wc -w`
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
    done
}
