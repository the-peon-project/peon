#!/bin/bash
source cli/shared.sh
source cli/peon.sh
source cli/game.sh

menu_main() {
    draw_menu_header $menu_size "$app_name" "M A I N - M E N U"
    printf " 1. List All Containers\n"
    printf " 2. Peon Application Containers\n"
    printf " 3. Game Containers\n"
    printf " 0. Exit\n\n"
}

menu_main_read_options() {
    local choice
    read -p "Enter selection: " choice
    case $choice in
    0)
        clear
        exit 0
        ;;
    1) list_all_containers ;;
    2) menu_peon ;;
    3) menu_game ;;
    *) printf "\n ${RED_HL}*Invalid Option*${STD}\n" && sleep 0.75 ;;
    esac
}

trap 'exit 0' SIGINT SIGQUIT SIGTSTP
while true; do

    if [ -z "$1" ]; then
        menu_main
        menu_main_read_options
    else
        case "$1" in
        -u | --update)
            peon_update_containers
            exit $?
            ;;
        -s | --start)
            peon_start_containers
            exit $?
            ;;
        -p | --stop)
            peon_stop_containers
            exit $?
            ;;
        -r | --restart)
            peon_restart_containers
            exit $?
            ;;
        -m | --metrics)
            peon_get_metrics
            exit $?
            ;;       
        -* | --*=) # unsupported flags
            echo "ERROR: $1 is not supported." >&2
            printf " Supported flags are:\n\t-u|--update\tupdates peon containers\n\t-s|--start\tstarts peon conatiners\n\t-p|--stop\tstops peon containers\n\t-r|--restart\trestarts peon containers\n"
            exit 1
            ;;
        esac
    fi
    exit 0
done
