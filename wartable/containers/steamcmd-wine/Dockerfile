# wartable/containers/steamcmd-wine/Dockerfile
ARG BASE_VERSION=latest
FROM umlatt/peon-steamcmd-base:${BASE_VERSION}
LABEL "com.peon.description"="Peon Steamcmd & Wine HQ"
USER root
# Overlay this variant's own branded motd/banner on top of the base's generic one.
COPY ./media/motd /etc/motd
RUN apt-get update && apt-get install -y --no-install-recommends gnupg xvfb lib32gcc-s1 libstdc++6
RUN dpkg --add-architecture i386
RUN curl -fsSL https://dl.winehq.org/wine-builds/winehq.key | gpg --dearmor -o /usr/share/keyrings/winehq-archive-keyring.gpg
RUN DEBIAN_VERSION=$(cat /etc/os-release | grep '^VERSION_CODENAME=' | cut -d '=' -f 2) && echo "deb [signed-by=/usr/share/keyrings/winehq-archive-keyring.gpg] https://dl.winehq.org/wine-builds/debian/ $DEBIAN_VERSION main" > /etc/apt/sources.list.d/winehq.list
RUN apt-get update && apt-get install -y --install-recommends winehq-stable
RUN mkdir /tmp/.X11-unix && chmod 1777 /tmp/.X11-unix
RUN export PATH=$PATH:/opt/wine-stable/bin
ENV OS_TYPE=windows
# ----------------------------------------
USER steam
RUN mkdir -p /home/steam/config/
ENV CONTAINER_TYPE="umlatt/steamcmd-winehq"
ARG VERSION
ENV VERSION=${VERSION}
RUN echo VERSION=${VERSION} >> /etc/environment
ENTRYPOINT [ "/bin/bash", "/init/entrypoint"]
