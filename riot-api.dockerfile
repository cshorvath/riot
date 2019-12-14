FROM python:3.8-slim

WORKDIR /opt/riot


RUN apt-get -y update && apt-get -y install g++

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./service/core ./core
COPY ./service/api ./api
COPY example_config/api.yaml ./config.yaml

ENV RIOT_API_CONFIG_FILE config.yaml
ENTRYPOINT  ["python3", "-m", "api"]