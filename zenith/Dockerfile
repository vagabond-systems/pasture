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

# configure openvpn
RUN apt -y install openvpn openresolv
COPY ./openvpn/configs /etc/openvpn/configs
COPY ./openvpn/login.conf /etc/openvpn/

# grab scripts
COPY ./scripts ./scripts
RUN chmod -R +x ./scripts

CMD ./scripts/bootstrapper.sh
