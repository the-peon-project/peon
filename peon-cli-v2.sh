#!/bin/bash
source cli-v2/shared.sh

menu_main() {
    clear
    printf "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓\n"
    printf "┃          P E O N - C L I          ┃\n"
    printf "┗━━━━━━━┯━━━━━━━━━━━━━━━━━━━┯━━━━━━━┛\n"
    printf "        │ M A I N - M E N U │\n"
    printf "        └───────────────────┘\n"
    printf " 1. List All Containers\n"
    printf " 2. Peon Containers\n"
    printf " 2. Game Containers\n"
    printf " 0. Exit\n\n"
}

main_menu_read_options() {
    local choice
    read -p "Enter selection: " choice
    case $choice in
    0) exit 0 ;;
    1) list_all_containers ;;
    2) two ;;
    *) printf "${RED_HL}Error...${STD}\n" && sleep 2 ;;
    esac
}

trap '' SIGINT SIGQUIT SIGTSTP
while true
do
	menu_main
	main_menu_read_options
done