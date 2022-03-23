#!/bin/bash
# Create working folders
mkdir servers
mkdir recipies
# Pull latest recipies from github project and stage to folder
cd recipies
wget https://github.com/nox-noctua-consulting/peon-recipies/archive/master.tar.gz
tar -xvf master.tar.gz --strip-components=1
rm -rf master.tar.gz