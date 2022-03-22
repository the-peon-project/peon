#!/bin/bash
script="${0##*/}"
logfile="/var/log/peon/$script.log"
echo "Updating steamcmd." >> $logfile
./steamcmd.sh +app_update +quit >> $logfile
echo "Installing/configuring the game server." >> $logfile
./steamcmd.sh +force_install_dir /data +login anonymous +app_update 740 +quit >> $logfile
echo "Adding server ready file, for hand back"
echo "READY" > ./data/server.state
echo "Processing complete." >> $logfile