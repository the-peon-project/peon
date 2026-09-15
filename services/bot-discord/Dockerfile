# Base image debian bullseye slim
FROM python:3.11-slim-bullseye
# Build information
LABEL "com.peon.description"="Peon Bot - Discord"
LABEL "maintainer"="Umlatt <richard@lazylionconsulting.com>"
# Copy "branding" stuff
COPY ./media/motd /etc/motd
RUN echo "cat /etc/motd" >> /etc/bash.bashrc
# Install python requirements
COPY ./requirements.txt /app/requirements.txt
# Update pip and install required python modules
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip3 install --no-cache-dir --upgrade -r /app/requirements.txt
# Install required tools
RUN apt-get update && apt-get -y install ssh
# TEMP: Install debug tools
RUN apt-get update && apt-get -y install procps iputils-ping dnsutils vim
# Configure version
ENV CONTAINER_TYPE="bot.discord"
ARG VERSION
ENV VERSION=${VERSION}
RUN echo VERSION=${VERSION} >> /etc/environment
# Start the app called api
COPY ./app /app
# Move to working directory
WORKDIR /app
# Start application
CMD ["/bin/sh", "-c","python3 main.py"]