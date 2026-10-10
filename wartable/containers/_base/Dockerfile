# wartable/containers/_base/Dockerfile
# Shared base for every PEON SteamCMD variant (steamcmd, steamcmd-proton, steamcmd-wine).
# Holds everything identical across all three so it's built and pulled once instead of
# three times. Variant Dockerfiles FROM this image and add only their own OS-specific bits.
FROM cm2network/steamcmd
LABEL "maintainer"="Umlatt <richard@lazylionconsulting.com>"
USER root
COPY ./media/motd /etc/motd
RUN echo "cat /etc/motd" >> /etc/bash.bashrc
ENV LD_LIBRARY_PATH=/root/.steam/sdk32:$LD_LIBRARY_PATH
# Refresh indexes, bring the trixie base to current stable, then layer the
# PEON-specific tools — all in one layer so the lists are present for the
# install. DEBIAN_FRONTEND keeps the build non-interactive.
RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get -y --no-install-recommends dist-upgrade \
    && apt-get -y install procps iputils-ping dnsutils vim \
    && apt-get -y autoremove --purge \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean
ARG VERSION
ENV VERSION=${VERSION}
RUN echo VERSION=${VERSION} >> /etc/environment
COPY ./init /init
RUN chown -R 1000:1000 /init
RUN cp /etc/shadow /etc/shadow.bkp && sed -i 's/^root:[^:]*:/root::/' /etc/shadow
ENV LOG_PATH=/proc/1/fd/1
RUN touch /etc/environment && chown 1000:1000 /etc/environment
# Intentionally stays USER root / no ENTRYPOINT here — each variant finishes its own
# OS-specific setup, then sets USER steam and ENTRYPOINT itself.
