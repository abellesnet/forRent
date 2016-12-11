# forRent

#### A home renting app

## Microservices and Docker

This app consists of three microservices:

* APIGateway
* Broker (RabbitMQ)
* Worker (ImageProcessor)

These microservices can run in an isolated Docker containers. You can start the containers using the script in `start_services.sh`.

Other useful commands:

* Scale the ImageProcessor worker:
`docker-compose scale imageprocessor=2`

* Open a container console:
`docker exec -it $(docker ps -q -f name=forrent_api_gateway) /bin/bash`

* Force running containers to stop:
`docker-compose kill`

## Samples

You can avoid start from scratch. The project includes a command to load samples. You must run it inside the APIGateway container:
`python manage.py load_samples --settings=forrent.settings_prod`

## API urls

`/room/api/1.0/`

## Changelog

v2.0
* Rent a room

v1.1
* User profile with photo

v1.0
* User management
* Room CRUD
* Image optimization
* Internationalization
* Microservices
* Amazon ECS with Doker deploy