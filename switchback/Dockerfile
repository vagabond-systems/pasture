FROM ubuntu:jammy

RUN apt -y update
RUN apt -y upgrade
RUN apt -y install \
    bash \
    git \
    vim \
    curl \
    systemctl \
    sudo

WORKDIR /app

# configure squid
RUN apt -y install squid
COPY squid.conf /etc/squid/squid.conf
RUN systemctl enable squid

# grab scripts
COPY ./scripts ./scripts
RUN chmod -R +x ./scripts

CMD ./scripts/bootstrapper.sh
