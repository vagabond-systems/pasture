FROM python:3.11-slim
ENV PYTHONUNBUFFERED True
WORKDIR /app

RUN apt -y update
RUN apt -y upgrade
RUN apt -y install \
    gcc \
    libpq-dev \
    python3-dev \
    python3-pip

COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ .
CMD exec gunicorn --bind 0.0.0.0:33033 --workers 1 entrypoint:app
