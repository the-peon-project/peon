#!/bin/bash
## ----------------------------------
# Step #1: Define variables
# ----------------------------------
STD='\033[0;0;39m'
RED_HL='\033[0;41;30m'
GREEN_HL='\033[0;41;30m'
BLUE='\033[0;34m'
RED='\033[0;31m'
GREEN='\033[0;32m'

pause() {
    read -p "Press [Enter] key to continue..." fackEnterKey
}

one() {
    printf "one() called"
}

# do something in two()
two() {
    printf "two() called"
}

# function to display menus
main_menu() {
    clear
    printf "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓\n"
    printf "┃          P E O N - C L I          ┃\n"
    printf "┗━━━━━━━┯━━━━━━━━━━━━━━━━━━━┯━━━━━━━┛\n"
    printf "        │ M A I N - M E N U │\n"
    printf "        └───────────────────┘\n"
    printf " 1. Set Terminal\n"
    printf " 2. Reset Terminal\n"
    printf " 0. Exit\n\n"
}

read_mm_options() {
    local choice
    read -p "Enter selection " choice
    case $choice in
    0) exit 0 ;;
    1) one ;;
    2) two ;;
    *) printf "${RED_HL}Error...${STD}\n" && sleep 2 ;;
    esac
}
