# wartable/containers/_shared/init/lib/server_start_lib.sh
# Sourced by warplans/<game>/actions/server_start for native-Linux SteamCMD games.
# Baked into every game-server image at /init/lib/server_start_lib.sh via the
# shared steamcmd base image (see wartable/containers/_base/Dockerfile).

peon_server_starting() {
    # $1: human-readable game name, e.g. "Ark"
    echo "###### Server ${1}.$SERVER_NAME [STARTING]"
}

peon_steam_ld_path_enter() {
    export templdpath=$LD_LIBRARY_PATH
    export LD_LIBRARY_PATH=./linux64:$LD_LIBRARY_PATH
}

peon_steam_ld_path_exit() {
    export LD_LIBRARY_PATH=$templdpath
}
