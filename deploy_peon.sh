#!/bin/bash

get_compose_command() {
    if command -v docker-compose >/dev/null 2>&1; then
        echo "docker-compose"
        return 0
    fi
    if command -v docker >/dev/null 2>&1 && docker compose version >/dev/null 2>&1; then
        echo "docker compose"
        return 0
    fi
    return 1
}

ensure_env_defaults() {
    local sample_file=".env.sample"
    local env_file=".env"

    if [ ! -f "$env_file" ]; then
        cp "$sample_file" "$env_file"
        return 0
    fi

    while IFS= read -r line || [ -n "$line" ]; do
        case "$line" in
            ""|\#*) continue ;;
        esac

        key="${line%%=*}"
        if ! grep -q "^${key}=" "$env_file"; then
            printf "\n%s\n" "$line" >> "$env_file"
        fi
    done < "$sample_file"
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

help_information() {
    echo "Usage: $0 [OPTIONS]"
    echo "  -o, --orchestrator   Enable PEON Orchestrator"
    echo "  -k, --apikey <key>   Configure custom PEON Orchestrator API key (defaults to 'Zu88Zu88')"
    echo "  -w, --webui          Enable PEON Web User Interface"
    echo "  -p, --proxy          Enable reverse proxy with automatic Let's Encrypt certificates"
    echo "  -m, --proxy-domain   Public domain for reverse proxy (e.g. server.example.com)"
    echo "  -e, --proxy-email    Email used for Let's Encrypt registration"
    echo "  -c, --cache          Enable shared download cache proxy"
    echo "  -d, --documentation  Enable PEON documentation"
    echo "  -1, --dbot           Enable PEON Discord bot"
    echo "  -h, --help           Show help"
    exit 0
}

# APP START
config_file_location="./config/docker-compose"
orc=false
web=false
proxy=false
cache=false
docs=false
bot_discord=false
apikey=""
proxy_domain=""
proxy_email=""
invalid="Invalid choice. Please try again.\n"
compose_command=$(get_compose_command)

if [ -z "$compose_command" ]; then
    echo "Docker Compose is not available. Install either 'docker compose' or 'docker-compose'."
    exit 1
fi

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
    if [[ "$web" = "true" ]]; then
        read -n 1 -p "Enable reverse proxy with automatic Let's Encrypt certificates? [y]/n: " choice
        printf "\n"
        case "$choice" in
            y|Y|""  ) proxy=true ;;
            n|N      ) proxy=false ;;
            *        ) printf "$invalid"; exit 1;;
        esac
    fi
    if [[ "$proxy" = "true" ]]; then
        read -p "Set reverse proxy domain (e.g. server.example.com): " proxy_domain_input
        if [ ! -z "$proxy_domain_input" ]; then
            proxy_domain=$proxy_domain_input
        else
            echo " [x] Reverse proxy domain is required when proxy is enabled."
            exit 1
        fi
        read -p "Set Let's Encrypt contact email: " proxy_email_input
        if [ ! -z "$proxy_email_input" ]; then
            proxy_email=$proxy_email_input
        else
            echo " [x] Let's Encrypt email is required when proxy is enabled."
            exit 1
        fi
    fi
    read -n 1 -p "Enable shared download cache proxy? [y]/n: " choice
    printf "\n"
    case "$choice" in
        y|Y|""  ) cache=true ;;
        n|N     ) cache=false ;;
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
    while getopts ":owpcd1:k:m:e:h-:" opt; do
        case ${opt} in
            o ) orc=true ;;
            w ) web=true ;;
            p ) proxy=true ;;
            c ) cache=true ;;
            d ) docs=true ;;
            1 ) bot_discord=true 
                discord_key=$OPTARG
                ;;
            k )
                apikey=$OPTARG
                ;;
            m )
                proxy_domain=$OPTARG
                ;;
            e )
                proxy_email=$OPTARG
                ;;
            h ) help_information; exit 0 ;;
            - )
                case ${OPTARG} in
                    orchestrator ) orc=true ;;
                    webui ) web=true ;;
                    proxy ) proxy=true ;;
                    cache ) cache=true ;;
                    documentation ) docs=true ;;
                    dbot ) bot_discord=true ;;
                    apikey )
                        apikey="${!OPTIND}"
                        OPTIND=$(($OPTIND+1))
                        ;;
                    proxy-domain )
                        proxy_domain="${!OPTIND}"
                        OPTIND=$(($OPTIND+1))
                        ;;
                    proxy-email )
                        proxy_email="${!OPTIND}"
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

if [[ "$proxy" = "true" && "$web" != "true" ]]; then
    echo " [x] Reverse proxy requires web UI to be enabled."
    exit 1
fi

if [[ "$proxy" = "true" && ( -z "$proxy_domain" || -z "$proxy_email" ) ]]; then
    echo " [x] --proxy requires both --proxy-domain and --proxy-email in non-interactive mode."
    exit 1
fi

# APPLCATION
printf "# - AUTOMATICALLY GENERATED BY DEPLOYMENT SCRIPT-\n# - Changes here will be overwritten. - \n" > docker-compose.yml.tmp
cat "$config_file_location/01_network.yml"   >> docker-compose.yml.tmp
if [[ "$orc" = "true" ]]; then
    cat "$config_file_location/02_orc.yml"       >> docker-compose.yml.tmp
fi
if [[ "$web" = "true" ]]; then
    cat "$config_file_location/03_webui.yml"     >> docker-compose.yml.tmp
fi
if [[ "$proxy" = "true" ]]; then
    cat "$config_file_location/06_proxy.yml"     >> docker-compose.yml.tmp
fi
if [[ "$cache" = "true" ]]; then
    cat "$config_file_location/04_cache.yml"     >> docker-compose.yml.tmp
fi
if [[ "$docs" = "true" ]]; then
    cat "$config_file_location/05_docs.yml"      >> docker-compose.yml.tmp
fi
if [[ "$bot_discord" = "true" ]]; then
    cat "$config_file_location/20_bots.yml"      >> docker-compose.yml.tmp
fi
if [[ "$cache" = "true" || "$proxy" = "true" ]]; then
    printf "\n" >> docker-compose.yml.tmp
    cat <<'EOF' >> docker-compose.yml.tmp
volumes:
EOF
        if [[ "$cache" = "true" ]]; then
                cat <<'EOF' >> docker-compose.yml.tmp
    peon-cache-squid:
EOF
        fi
        if [[ "$proxy" = "true" ]]; then
                cat <<'EOF' >> docker-compose.yml.tmp
    peon-proxy-data:
    peon-proxy-config:
EOF
        fi
fi
mv docker-compose.yml.tmp docker-compose.yml
rm -rf docker-compose.yml.tmp
# SETTINGS
ensure_env_defaults
if [[ "$cache" = "true" ]]; then
    sed -i "/PEON_CACHE_ENABLED/s/.*/PEON_CACHE_ENABLED=true/" .env
else
    sed -i "/PEON_CACHE_ENABLED/s/.*/PEON_CACHE_ENABLED=false/" .env
fi
if [[ "$proxy" = "true" ]]; then
    sed -i "/PEON_PROXY_ENABLED/s/.*/PEON_PROXY_ENABLED=true/" .env
    sed -i "/PEON_WEBUI_HOST_PORT/s/.*/PEON_WEBUI_HOST_PORT=8080/" .env
    sed -i "s|^PEON_PROXY_DOMAIN=.*|PEON_PROXY_DOMAIN=$proxy_domain|" .env
    sed -i "s|^PEON_PROXY_EMAIL=.*|PEON_PROXY_EMAIL=$proxy_email|" .env
else
    sed -i "/PEON_PROXY_ENABLED/s/.*/PEON_PROXY_ENABLED=false/" .env
    sed -i "/PEON_WEBUI_HOST_PORT/s/.*/PEON_WEBUI_HOST_PORT=80/" .env
fi
if [ ! -z "$apikey" ]; then
    sed -i "/PEON_API_KEY/s/.*/PEON_API_KEY='$apikey'/" .env
fi
if [ ! -z "$discord_key" ]; then
    sed -i "/DISCORD_TOKEN/s/.*/DISCORD_TOKEN='$discord_key'/" .env
fi
printf "\n\n - Settings - "
cat .env
# CONFIGURE BANNER
if [ -w /etc/motd ]; then
    cat "./media/banner" > /etc/motd
elif command -v sudo >/dev/null 2>&1 && sudo -n true >/dev/null 2>&1; then
    sudo tee /etc/motd >/dev/null < "./media/banner"
else
    echo " [!] Skipping /etc/motd update; elevated write access is not available."
fi
# ADD PEON ENV
echo "alias peon='docker exec -it peon.orc peon'" >> ~/.bashrc
source ~/.bashrc
# START UP APPLICATION
$compose_command up --remove-orphans -d

