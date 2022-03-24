#!/bin/bash
STD='\033[0;0;39m'
RED_HL='\033[0;41;30m'
GREEN_HL='\033[0;41;30m'
BLUE='\033[0;34m'
RED='\033[0;31m'
GREEN='\033[0;32m'

pause() {
    printf "\n"
    read -p "Press [Enter] key to continue..." fackEnterKey
}

list_all_containers() {
    clear
    printf "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓\n"
    printf "┃          P E O N - C L I          ┃\n"
    printf "┗━┯━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┯━┛\n"
    printf "  │  A L L   C O N T A I N E R S  │\n"
    printf "  └───────────────────────────────┘\n"
    docker ps -a --format "table {{.Names}}\t{{.State}}"
    pause
}

# do something in two()
two() {
    printf "two() called"
}
