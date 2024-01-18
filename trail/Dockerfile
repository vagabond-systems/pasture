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

# install requirements
COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# grab source
COPY ./src ./src
COPY ./bootstrapper.sh ./bootstrapper.sh

CMD ./bootstrapper.sh
