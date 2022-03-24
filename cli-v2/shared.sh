#!/bin/bash
STD='\033[0;0;39m'
RED_HL='\033[0;41;30m'
GREEN_HL='\033[0;41;30m'
BLUE='\033[0;34m'
RED='\033[0;31m'
GREEN='\033[0;32m'
menu_size=40
app_name="P E O N - C L I"

pause() {
    printf "\n"
    read -p "Press [Enter] key to continue..." fackEnterKey
}

draw_menu_header() {
    clear
    width=$1 title=$2 heading=$3 bar_heavy="" bar_light=""
    if (( ${#title} % 2 )) ; then title+=" "; fi
    if (( ${#heading} % 2 )) ; then heading+=" "; fi
    title_size=${#title} heading_size=${#heading}
    if (( $width < $title_size )); then width=$title_size; fi
    if (( $width < $heading_size )); then width=$heading_size; fi
    width=$(($width+8))
    for ((i = 1; i <= $width; i++)); do bar_heavy+="━"; done
    for ((i = 1; i <= $(($width - 4)); i++)); do bar_light+="─"; done
    mid_bar=$(sed -e "s/./┯/2" <<<$bar_heavy)
    mid_bar=$(sed -e "s/./┯/$(($width - 1))" <<<$mid_bar)
    title_gap=$(printf "%*s%s" $((($width - $title_size) / 2)) '' "$line")
    heading_gap=$(printf "%*s%s" $((($width - $heading_size - 4) / 2)) '' "$line")
    printf "┏$bar_heavy┓\n┃$title_gap$title$title_gap┃\n┗$mid_bar┛\n  │$heading_gap$heading$heading_gap│\n  └$bar_light┘\n"
}

list_all_containers() {
    draw_menu_header $menu_size "$app_name" "A L L   C O N T A I N E R S"
    docker ps -a --format "table {{.Names}}\t{{.State}}"
    pause
}
