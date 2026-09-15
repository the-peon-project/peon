#!/bin/bash
logfile="/var/log/peon/${0##*/}.log"
rootpath="/home/steam/steamcmd/"
cd $rootpath
echo "" > $logfile
# Logging config start - capture all
exec 3>&1 4>&2
trap 'exec 2>&4 1>&3' 0 1 2 3
exec 1>>$logfile 2>&1
# Logging config end
echo "##################### STARTING SERVER ######################"
# Create a server.config file which contains relevant connection info for gamers (in the config directory)
conf_file="/home/steam/config/server.config"
printf "IP [$PUBLIC_IP]" > $conf_file
# CUSTOM GAME SERVER COMMAND
cd ./data/linux/ && ./starbound_server 
