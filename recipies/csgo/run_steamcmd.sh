#!/bin/bash
script="${0##*/}"
mkdir -p data/docker/logs
logfile="./data/docker/logs/$script.log"
echo "Updating steamcmd." >> $logfile
./steamcmd.sh +app_update +quit
echo "Installing/configuring the game server." >> $logfile
./steamcmd.sh +force_install_dir /data +login anonymous +app_update 740 +quit >> $logfile
echo "Adding server ready file, for hand back"
touch ./data/server.ready
echo "Processing complete." >> $logfile