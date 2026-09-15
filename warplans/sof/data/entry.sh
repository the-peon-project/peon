#!/bin/bash
set -x

echo "Sons of the Forest Dedicated Server - PEON Warplan"
echo "Using Docker image: jammsen/sons-of-the-forest-dedicated-server"

# The Docker image handles server installation and startup
# This script just ensures config files are in place

# Create config directory if it doesn't exist
mkdir -p /home/steam/.config/unity3d/Endnight/SonsOfTheForestDS

# Copy server configuration
if [ -f "${STEAMAPPDIR}/server.cfg" ]; then
    echo "Copying server configuration..."
    cp "${STEAMAPPDIR}/server.cfg" /home/steam/.config/unity3d/Endnight/SonsOfTheForestDS/dedicatedserver.cfg
fi

# Pre Hook
if [ -f "${STEAMAPPDIR}/pre.sh" ]; then
    source "${STEAMAPPDIR}/pre.sh"
fi

echo "Configuration complete. Server will start via Docker image."

# Post Hook  
if [ -f "${STEAMAPPDIR}/post.sh" ]; then
    source "${STEAMAPPDIR}/post.sh"
fi