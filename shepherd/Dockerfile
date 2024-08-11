FROM ubuntu:jammy

RUN apt -y update
RUN apt -y upgrade
RUN apt -y install \
    bash \
    git \
    vim \
    curl \
    systemctl \
    sudo \
    gcc \
    libpq-dev \
    python3-dev \
    python3-pip

WORKDIR /app

COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src
CMD python3 /app/src
