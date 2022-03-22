#!/bin/bash
# Get script name for logging
script="${0##*/}"
rootpath=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
# Get parameters
PARAMS=""
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


logfile="/var/log/peon/deploy-$game-$servername.log"
server_path="$rootpath/$game/$servername"
container="peon.$game.$servername"
mkdir -p $server_path
#chown -R docker:docker $servername
echo "Created data path: [$server_path]" >> $logfile
echo "Starting container/s..." >> $logfile
docker run -t -v "$server_path":/data --name "$container" cm2network/steamcmd
docker exec $container mkdir serverdata
docker exec $container  ./steamcmd +login anonymous +force_install_dir /data +app_update 740 +quit
echo "Process complete" >> $logfile