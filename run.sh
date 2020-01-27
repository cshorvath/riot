API_CONTAINER_NAME=riot-api
DS_CONTAINER_NAME=riot-data-processor
UI_CONTAINER_NAME=riot-ui

docker rm -f $UI_CONTAINER_NAME
docker rm -f $API_CONTAINER_NAME
docker rm -f $DS_CONTAINER_NAME

docker run --name $API_CONTAINER_NAME --net=host -d -it riot_api:latest
docker run --name $UI_CONTAINER_NAME --net=host -d riot_ui
docker run --name $DS_CONTAINER_NAME --net=host -d riot_data_processor:latest
