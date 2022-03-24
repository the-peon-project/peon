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

draw_menu_header() {
    width=$1 title=$2 heading=$3 bar_heavy="" bar_light="" even_space=""
    title_size=${#title} heading_size=${#heading}
    if ! (( $width % 2 )) ; then even_space=" "; fi
    for ((i = 1; i <= $width; i++)); do bar_heavy+="━"; done
    for ((i = 1; i <= $(($width - 4)); i++)); do bar_light+="─"; done
    mid_bar=$(sed -e "s/./┯/2" <<<$bar_heavy)
    mid_bar=$(sed -e "s/./┯/$(($width - 1))" <<<$mid_bar)
    title_gap=$(printf "%*s%s" $((($width - $title_size) / 2)) '' "$line")
    heading_gap=$(printf "%*s%s" $((($width - $heading_size - 4) / 2)) '' "$line")
    printf "┏$bar_heavy┓\n┃$title_gap$title$title_gap$even_space┃\n┗$mid_bar┛\n"
    printf "  │$heading_gap$heading$heading_gap$even_space│  \n  └$bar_light┘\n"
    pause
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
