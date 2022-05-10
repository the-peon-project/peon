#!/bin/bash
# Configure logging
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
# Set permissions for docker containers
chown -R 1000:1000 .
# Deploy peon infrastructure
docker-compose up -d
#
# O R C - A U T H E N T I C A T I O N
#
./configure_orc.sh
#
# P E O N - C L I
#
echo "#!/bin/bash" > /usr/bin/peon
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
echo "$SCRIPT_DIR/peon-cli.sh \"\$@\"" >> /usr/bin/peon
sudo chomd +x /usr/bin/peon
#
# MESSAGE OF THE DAY (LOGIN BANNER)
#
sudo cat "$SCRIPT_DIR/media/banner" > /etc/motd

##!/bin/bash
#cd /root/peon/
#./peon-cli.sh "$@"