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

if [ -z ${game+x} ] ; then 
    echo "Not all parameters were passed."
    exit
fi
# Logging config start - Create logfile and capture all stdout to it
logfile="/var/log/peon/$script.log"
exec 3>&1 4>&2
trap 'exec 2>&4 1>&3' 0 1 2 3
exec 1>>$logfile 2>&1
# Logging config end

# Create a directory, so Git doesn't get messy, and enter it
mkdir ../servers/$game && cd ../servers/$game
# Start a Git repository
git init
# Track repository, do not enter subdirectory
git remote add -f origin https://github.com/nox-noctua-consulting/peon
# Enable the tree check feature
git config core.sparseCheckout true
echo 'recipies/'$game >> .git/info/sparse-checkout

## Download with pull, not clone
git pull origin master
