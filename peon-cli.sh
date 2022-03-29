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
    menu_main
    menu_main_read_options
done
