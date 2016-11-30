#!/bin/bash
# start microservices on development

# remove old project containers, if they exist
docker rm -f $(docker ps -q -a -f name=forrent)

# remove all dangling images, if they exist
docker rmi -f $(docker images -q -a -f dangling=true)

# build images
docker-compose build --force-rm --pull

# start containers
docker-compose up --force-recreate --remove-orphans

# OTHER COMMANDS:

# scale the imageprocessor worker
#docker-compose scale imageprocessor=2

# open a container console
#docker exec -it $(docker ps -q -f name=forrent_api_gateway) /bin/bash

# force running containers to stop
#docker-compose kill
