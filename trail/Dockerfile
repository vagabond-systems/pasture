FROM ubuntu:jammy

RUN apt -y update
RUN apt -y upgrade
RUN apt -y install \
    bash \
    git \
    vim \
    python3-dev \
    python3-pip \
    curl \
    htop \
    unzip \
    nmap \
    systemctl \
    sudo


WORKDIR /app

# configure squid
RUN apt -y install squid
COPY squid.conf /etc/squid/squid.conf
RUN systemctl enable squid

# configure openvpn
RUN apt -y install openvpn openresolv
COPY ./openvpn/configs /etc/openvpn/configs
COPY ./openvpn/login.conf /etc/openvpn/
COPY ./openvpn/resolv.conf /etc/openvpn/

# install requirements
COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# grab scripts
COPY ./scripts ./scripts
RUN chmod -R +x ./scripts

CMD ./scripts/bootstrapper.sh
