#!/bin/bash
# Configure logginf
logfile="/var/log/peon/${0##*/}.log"
echo "Progress log in $logfile"
exec 3>&1 4>&2
trap 'exec 2>&4 1>&3' 0 1 2 3
exec 1>>$logfile 2>&1
# Create working directories
mkdir servers
mkdir plans
# Pull latest plans from github project and stage to folder
wget https://github.com/nox-noctua-consulting/peon-plans/archive/master.tar.gz
tar -xvf master.tar.gz --strip-components=1 --directory plans
rm -rf master.tar.gz
# docker-compose up -d
# Set permissions for docker containers
chown -R 1000:1000 .