#!/bin/bash
source cli-v2/shared.sh
source cli-v2/peon.sh
source cli-v2/game.sh

menu_main() {
    clear
    printf "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓\n"
    printf "┃          P E O N - C L I          ┃\n"
    printf "┗━━━━━━━┯━━━━━━━━━━━━━━━━━━━┯━━━━━━━┛\n"
    printf "        │ M A I N - M E N U │\n"
    printf "        └───────────────────┘\n"
    printf " 1. List All Containers\n"
    printf " 2. Peon Containers\n"
    printf " 3. Game Containers\n"
    printf " 0. Exit\n\n"
}

main_menu_read_options() {
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
    4) draw_menu_header 35 "P E O N - C L I" "A L L   C O N T A I N E R S" ;;
    *) printf "\n ${RED_HL}*Invalid Option*${STD}\n" && sleep 0.75 ;;
    esac
}

trap '' SIGINT SIGQUIT SIGTSTP
while true; do
    menu_main
    main_menu_read_options
done
