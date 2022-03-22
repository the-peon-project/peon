#!/bin/bash
# Get script name for logging
script="${0##*/}"
rootpath=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
# Get parameters
PARAMS=""
overwrite=false
while (( "$#" )); do
  case "$1" in
    -g|--game)
      if [ -n "$2" ] && [ ${2:0:1} != "-" ]; then
        game=$2
        shift 2
      else
        echo "Error: Argument for $1 is missing" >&2
        exit 1
      fi
      ;;
    -n|--server-name)
      if [ -n "$2" ] && [ ${2:0:1} != "-" ]; then
        servername=$2
        shift 2
      else
        echo "Error: Argument for $1 is missing" >&2
        exit 1
      fi
      ;;
    -o|--overwrite)
      overwrite=true
      shift
      ;;
    -*|--*=) # unsupported flags
      echo "Error: Unsupported flag $1" >&2
      exit 1
      ;;
    *) # preserve positional arguments
      PARAMS="$PARAMS $1"
      shift
      ;;
  esac
done
# set positional arguments in their proper place
eval set -- "$PARAMS"

if [ -z ${game+x} ] || [ -z ${servername+x} ] ; then 
    echo "Not all parameters were passed."
    exit
fi
mkdir -p /var/log/peon/$game/$servername
chown -R 1000:1000 /var/log/peon
logfile="/var/log/peon/$game/$servername/$script.log"
server_path="$rootpath/$game/$servername"
container="peon.$game.$servername"
containers=`docker ps -a | grep -i $container`
if [ "$containers" ] && $overwrite ; then
    echo "Container exists, but overwrite configured. Removing containers before proceeding." >> $logfile
    docker stop $container
    docker rm $container
    rm -rf $server_path/server.state
fi
containers=`docker ps -a | grep -i $container`
if [ -z "$containers" ]; then
    echo "Creating data paths: [$server_path]" >> $logfile
    mkdir -p $server_path
    chown -R 1000:1000 $server_path
    echo "Starting container/s..." >> $logfile
    docker run -dit -v $server_path:/home/steam/steamcmd/data -v /var/log/peon/$game/$servername:/var/log/peon --name $container --user steam cm2network/steamcmd >> $logfile
    echo "Adding deploy code to container." >> $logfile
    docker cp run_steamcmd.sh $container:/home/steam/steamcmd/.
    echo "Run 'run_steamcmd.sh in container.'" >> $logfile
    docker exec -d --workdir /home/steam/steamcmd --user steam $container bash run_steamcmd.sh
else
    echo "Container already exists. Exiting." >> $logfile
fi
echo "Script comeplete." >> $logfile

# Docker container recommmended in - https://developer.valvesoftware.com/wiki/SteamCMD#Docker