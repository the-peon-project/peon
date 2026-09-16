# BASE: Base image - Python (Debian + slim)
FROM python:3.11-slim-bullseye
# CONTAINER: Configuration
LABEL "com.peon.description"="Peon Orchestrator"
LABEL "maintainer"="Umlatt <richard@lazylionconsulting.com>"
# BRANDING: Copy branding into container
COPY ./media/motd /etc/motd
RUN echo "cat /etc/motd" >> /etc/bash.bashrc
# OS: Prepare the OS and middleware
# Debian bullseye is EOL; deb.debian.org no longer serves it. Pin apt to a snapshot.
RUN printf 'deb http://snapshot.debian.org/archive/debian/20250721T000000Z bullseye main\ndeb http://snapshot.debian.org/archive/debian-security/20250721T000000Z bullseye-security main\ndeb http://snapshot.debian.org/archive/debian/20250721T000000Z bullseye-updates main\n' > /etc/apt/sources.list
RUN echo 'Acquire::Check-Valid-Until "false";' > /etc/apt/apt.conf.d/99no-check-valid-until
RUN apt-get update
# DOCKER
RUN apt-get install -y apt-transport-https ca-certificates curl gnupg lsb-release subversion bsdmainutils zip
RUN curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
RUN echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
RUN apt-get update && apt-get install -y docker-ce docker-ce-cli containerd.io
# PYTHON
COPY ./requirements.txt /app/requirements.txt
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip3 install --no-cache-dir --upgrade -r /app/requirements.txt
# DEBUG: Install tools for debugging
RUN apt-get update && apt-get -y install procps iputils-ping dnsutils vim
# APPLICATION
COPY ./app /app
WORKDIR /app
ENV PATH="/app/bin:${PATH}"
# BUILD ERROR NOTE: historically required peon-cli/bin to be bind-mounted into ./app build directory (e.g. `/home/USER/development/peon-cli/bin /home/USER/development/peon-orc/app/bin none bind 0 0`); app/bin now ships committed copies of peon/cli/bin instead, so this mount is no longer needed (see peon/services/orc/CLAUDE.md, "Warplan Source" section, for the known duplication this leaves behind)
RUN mkdir -p /app/bin/config && echo "/home/peon/servers/" > /app/bin/config/peon_dir 
# BACKWARDS COMPATIBILITY
RUN echo "alias docker-compose='docker compose'" >> /etc/bash.bashrc
RUN echo "alias docker-compose='docker compose'" >> /etc/profile
# VERSION
ENV CONTAINER_TYPE="orchestrator"
ARG VERSION
ENV VERSION=${VERSION}
RUN echo VERSION=${VERSION} >> /etc/environment
# Start application
COPY ./init /init
CMD ["/bin/bash","/init/peon.orc"]