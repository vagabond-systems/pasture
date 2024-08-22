FROM python:3.11-slim
ENV PYTHONUNBUFFERED True
WORKDIR /app

RUN apt -y update
RUN apt -y upgrade

COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ .
CMD exec gunicorn --bind 0.0.0.0:23000 --workers 1 --timeout 0 entrypoint:app
