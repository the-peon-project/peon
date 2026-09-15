# wartable/containers/steamcmd/Dockerfile
ARG BASE_VERSION=latest
FROM umlatt/peon-steamcmd-base:${BASE_VERSION}
LABEL "com.peon.description"="Peon SteamCMD"
USER root
# Overlay this variant's own branded motd/banner on top of the base's generic one.
COPY ./media/motd /etc/motd
USER steam
RUN mkdir -p /home/steam/config/
ENV CONTAINER_TYPE="umlatt/steamcmd"
ARG VERSION
ENV VERSION=${VERSION}
RUN echo VERSION=${VERSION} >> /etc/environment
ENTRYPOINT [ "/bin/bash", "/init/entrypoint"]
