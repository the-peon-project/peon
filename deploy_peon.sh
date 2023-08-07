#!/bin/bash

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

help_information() {
    echo "Usage: $0 [OPTIONS]"
    echo "  -o, --orchestrator   Enable PEON Orchestrator"
    echo "  -k, --apikey <key>   Configure custom PEON Orchestrator API key (defaults to 'Zu88Zu88')"
    echo "  -w, --webui          Enable PEON Web User Interface"
    echo "  -d, --documentation  Enable PEON documentation"
    echo "  -1, --dbot           Enable PEON Discord bot"
    echo "  -h, --help           Show help"
    exit 0
}

# APP START
config_file_location="./config/docker-compose"
orc=false
web=false
docs=false
bot_discord=false
apikey=""
invalid="Invalid choice. Please try again.\n"

if [ "$#" -eq 0 ]; then
    draw_menu_header 35 "P E O N" "RE/CONFIGURE"
    read -n 1 -p "Enable Orchestrator (orc)? [y]/n: " choice
    printf "\n"
    case "$choice" in
        y|Y|""  ) orc=true ;;
        n|N     ) orc=false ;;
        *       ) printf "$invalid"; exit 1;;
    esac
    read -p "Set Orchestrator API key (enter for default): " apikey_input
    if [ ! -z "$apikey_input" ]; then
        apikey=$apikey_input
    fi
    read -n 1 -p "Enable Web Managament (webui)? [y]/n: " choice
    printf "\n"
    case "$choice" in
        y|Y|""  ) web=true ;;
        n|N     ) web=false ;;
        *       ) printf "$invalid"; exit 1;;
    esac
    read -n 1 -p "Enable Development Documentation (docs)? y/[n]: " choice
    printf "\n"
    case "$choice" in
        y|Y     ) docs=true ;;
        n|N|""  ) docs=false ;;
        *       ) printf "$invalid"; exit 1;;
    esac
    read -n 1 -p "Enable Bot - Discord (bot.discord)? [y]/n: " choice
    printf "\n"
    case "$choice" in
        y|Y|""  ) bot_discord=true 
                read -p "Configure Discord token: " discord_bot
                if [ ! -z "$discord_bot" ]; then
                    discord_key=$discord_bot
                else
                    echo " [x] A Discord bot Token must be provided."
                    exit 1
                fi;;
        n|N     ) bot_discord=false ;;
        *       ) printf "$invalid"; exit 1;;
    esac
else
    while getopts ":owd1:k:h-:" opt; do
        case ${opt} in
            o ) orc=true ;;
            w ) web=true ;;
            d ) docs=true ;;
            1 ) bot_discord=true 
                discord_key=$OPTARG
                ;;
            k )
                apikey=$OPTARG
                ;;
            h ) help_information; exit 0 ;;
            - )
                case ${OPTARG} in
                    orchestrator ) orc=true ;;
                    webui ) web=true ;;
                    documentation ) docs=true ;;
                    dbot ) bot_discord=true ;;
                    apikey )
                        apikey="${!OPTIND}"
                        OPTIND=$(($OPTIND+1))
                        ;;
                    help ) help_information; exit 0 ;;
                    * )
                        echo "Unknown parameter: --$OPTARG"
                        help_information
                        exit 1
                        ;;
                esac
                ;;
            * )
                echo "Unknown parameter: -$OPTARG"
                help_information
                exit 1
                ;;
        esac
    done
fi

printf "# - AUTOMATICALLY GENERATED BY DEPLOYMENT SCRIPT-\n# - Changes here will be overwritten. - \n" > docker-compose.yml.tmp
cat "$config_file_location/01_network.yml"   >> docker-compose.yml.tmp
if [[ "$orc" = "true" ]]; then
    cat "$config_file_location/02_orc.yml"       >> docker-compose.yml.tmp
fi
if [[ "$web" = "true" ]]; then
    cat "$config_file_location/03_webui.yml"     >> docker-compose.yml.tmp
fi
if [[ "$docs" = "true" ]]; then
    cat "$config_file_location/05_docs.yml"      >> docker-compose.yml.tmp
fi
if [[ "$bot_discord" = "true" ]]; then
    cat "$config_file_location/20_bots.yml"      >> docker-compose.yml.tmp
fi

mv docker-compose.yml.tmp docker-compose.yml
rm -rf docker-compose.yml.tmp

cp .env.sample .env
if [ ! -z "$apikey" ]; then
    sed -i "/PEON_API_KEY/s/.*/PEON_API_KEY=$apikey/" .env
fi
if [ ! -z "$discord_key" ]; then
    sed -i "/DISCORD_TOKEN/s/.*/DISCORD_TOKEN=$discord_key/" .env
fi

echo " - Settings - "
cat .env

# docker-compose up --remove-orphans -d