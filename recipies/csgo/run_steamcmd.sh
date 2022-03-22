#!/bin/bash
# STEAM GAME ID
game_id='740'
#SCRIPT START
script="${0##*/}"
logfile="/var/log/peon/$script.log"
exec 3>&1 4>&2
trap 'exec 2>&4 1>&3' 0 1 2 3
exec 1>$logfile 2>&1

echo "Updating steamcmd."
stdbuf -oL ./steamcmd.sh +app_update +quit
echo "Installing/configuring the game server."
stdbuf -oL ./steamcmd.sh +force_install_dir ./data +login anonymous +app_update $game_id +quit
echo "Adding server ready file, for hand back"
echo "READY" > ./data/server.state
echo "Processing complete."