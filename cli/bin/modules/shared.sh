#!/bin/bash
STD='\033[0;0;39m'
RED_HL='\033[0;41;30m'
GREEN_HL='\033[0;41;30m'
BLUE='\033[0;34m'
RED='\033[0;31m'
GREEN='\033[0;32m'
ORANGE='\033[0;33m'
menu_size=35
app_name="P E O N - C L I"

pause() {
    printf "\n"
    read -p "Press [Enter] key to continue..." fackEnterKey
}

delay(){
    for i in $(seq 1 $1); do printf "."; sleep 1; done; echo ""
}

draw_menu_header() {
    clear
    width=$1 title=$2 heading=$3 bar_heavy="" bar_light=""                                                                  # Collect passed parameters and create empty strings
    if (($width % 2)); then width=$(($width + 1)); fi                                                                       # Make sure that width is even
    if ((${#title} % 2)); then title+=" "; fi                                                                               # Make sure that title has an even amount of characters (for formatting purposes)
    if ((${#heading} % 2)); then heading+=" "; fi                                                                           # Make sure that heading has an even amount of characters (for formatting purposes)
    title_size=${#title} heading_size=${#heading}                                                                           # Get the sizes of the title and the heading strings
    if (($width < $title_size)); then width=$title_size; fi                                                                 # If the title is bigger than the preset width, autoscale the width
    if (($width < $heading_size)); then width=$heading_size; fi                                                             # If the heading is bigger than the preset width, autoscale the width
    width=$(($width + 8))                                                                                                   # Set total menu width to include additional special characters
    for ((i = 1; i <= $width; i++)); do bar_heavy+="━"; done                                                                # Create the width of the heavy line for the box
    for ((i = 1; i <= $(($width - 4)); i++)); do bar_light+="─"; done                                                       # Create the width of the light line for the box
    mid_bar=$(sed -e "s/./┯/2" <<<$bar_heavy)                                                                               # Mid line for menu boxes. Insert first lower box anchor
    mid_bar=$(sed -e "s/./┯/$(($width - 1))" <<<$mid_bar)                                                                   # Mid line for menu boxes. Insert second lower box anchor
    title_gap=$(printf "%*s%s" $((($width - $title_size) / 2)) '' "$line")                                                  # Add whitespaces to centre the title text in the menu box
    heading_gap=$(printf "%*s%s" $((($width - $heading_size - 4) / 2)) '' "$line")                                          # Add whitespaces to centre the heading text in the menu box
    printf "┏$bar_heavy┓\n┃$title_gap$title$title_gap┃\n┗$mid_bar┛\n  │$heading_gap$heading$heading_gap│\n  └$bar_light┘\n" # Print out menu
}

centre_align_to_menu() {
    width=$1 text=$2
    text_size=${#text}
    spaces=""
    if (($width % 2)); then width=$(($width + 1)); fi
    if (($width > $text_size)); then
        width=$(($width + 8))
        spaces=$(printf "%*s%s" $((($width - $text_size) / 2)) '' "$line")
    fi
    echo "$spaces$text"
}

list_all_containers() {
    result=""
    while [ "$result" == "" ]; do
        draw_menu_header $menu_size "$app_name" "A L L   C O N T A I N E R S"
        docker ps -a --format "{{.Names}}\t{{.State}}" | sort | awk -F '\t' '{if ($2 == "exited") {$2 = "\033[31mexited\033[0m"} else if ($2 == "running") {$2 = "\033[32mrunning\033[0m"}; print $1 "\t" $2}' | column -t -s $'\t'

        read -n 1 -s -t 5 result
    done
}

run_command_as_root(){
    container=$1
    read -p "> " cmd
    docker exec -it -u root $container $cmd
    pause
}
