# wartable/containers/steamcmd-proton/Dockerfile
ARG BASE_VERSION=latest
FROM umlatt/peon-steamcmd-base:${BASE_VERSION}
LABEL "com.peon.description"="Peon Steamcmd & Proton (GE)"
USER root
# Overlay this variant's own branded motd/banner on top of the base's generic one.
COPY ./media/motd /etc/motd
RUN dpkg --add-architecture i386
RUN apt-get update && apt-get install --no-install-recommends -y ca-certificates winbind dbus libfreetype6 curl jq locales lib32gcc-s1 xvfb
RUN mkdir -p /tmp/.X11-unix && chmod 1777 /tmp/.X11-unix
RUN echo 'LANG="en_US.UTF-8"' > /etc/default/locale && echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen && locale-gen
RUN rm -f /etc/machine-id && dbus-uuidgen --ensure=/etc/machine-id
RUN rm -rf /var/lib/apt/lists/* && apt-get clean && apt-get autoremove -y
# Proton's entrypoint differs from the base/steamcmd default — overlay just that file.
COPY ./init/entrypoint /init/entrypoint
RUN chown 1000:1000 /init/entrypoint
USER steam
ENV STEAMCMD_PATH="/home/steam/steamcmd"
ENV STEAM_SDK64_PATH="/home/steam/.steam/sdk64"
ENV STEAM_SDK32_PATH="/home/steam/.steam/sdk32"
ENV OS_TYPE=windows
# ----------------------------------------
# PROTON GE
ENV GE_PROTON_VERSION "11-5"
ENV GE_PROTON_URL "https://github.com/GloriousEggroll/proton-ge-custom/releases/download/GE-Proton${GE_PROTON_VERSION}/GE-Proton${GE_PROTON_VERSION}-x86_64.tar.gz"
RUN mkdir "${STEAMCMD_PATH}/compatibilitytools.d/" && curl -fsSL "$GE_PROTON_URL" | tar xzvf - -C "${STEAMCMD_PATH}/compatibilitytools.d/"
RUN find "${STEAMCMD_PATH}/compatibilitytools.d/" -maxdepth 1 -type d -name "GE-Proton*" -exec mv {} "${STEAMCMD_PATH}/compatibilitytools.d/proton" \;
ENV STEAM_COMPAT_CLIENT_INSTALL_PATH "$STEAMCMD_PATH"
ENV STEAM_COMPAT_DATA_PATH "${STEAMCMD_PATH}/steamapps/compatdata/${STEAM_APP_ID}"
RUN mkdir -p $STEAM_COMPAT_DATA_PATH && chmod -R 755 $STEAM_COMPAT_DATA_PATH
ENV WINEDEBUG=-all
ENV UMU_ID 0
# ----------------------------------------
RUN mkdir -p /home/steam/config/
ENV CONTAINER_TYPE="umlatt/steamcmd-proton"
ARG VERSION
ENV VERSION=${VERSION}
RUN echo VERSION=${VERSION} >> /etc/environment
ENTRYPOINT [ "/bin/bash", "/init/entrypoint"]
