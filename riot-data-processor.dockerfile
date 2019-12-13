FROM python:3.8-slim

WORKDIR /opt/riot

RUN apt-get -y update && apt-get -y install g++

COPY ./requirements.txt ./
RUN pip install -r requirements.txt

COPY ./service/core ./core
COPY ./service/data_processor ./data_processor
COPY example_config/data_processor.yaml .

ENV RIOT_DATA_PROCESSOR_CONFIG data_processor.yaml
CMD ["python3", "-m", "data_processor"]