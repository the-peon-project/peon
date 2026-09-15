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
RUN apt-get update
RUN apt-get -y install procps iputils-ping dnsutils vim
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
