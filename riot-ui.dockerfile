FROM node:12.13.1-alpine3.9

COPY riot-ui /opt/riot/riot-ui
WORKDIR /opt/riot/riot-ui

RUN npm install

ARG api_url=http://localhost:8000
ARG port=8080
ENV REACT_APP_RIOT_API_URL $api_url
RUN npm run build

RUN npm install -g serve
CMD serve -s build -l 8080