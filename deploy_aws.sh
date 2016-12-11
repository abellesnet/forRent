#!/usr/bin/env bash
# deploy a new release on Amazon ECS

# IMPORTANT:
# This is a "how to" script that uses "abelles" production envinonment (Docker repos and AWS)
# If you want to deploy this app, you must write your own scripts

# usage:
# ./deploy_aws.sh tag
# example:
# ./deploy_aws.sh 1.0

if [ -z "$1" ]
then
    echo "Tag missing"
else

    echo "Deploying $1 version"

    docker build ./forrent --force-rm --pull -t abelles/forrent:$1

    docker build ./imageprocessor --force-rm --pull -t abelles/forrent-imageprocessor:$1

    docker push abelles/forrent:$1

    docker push abelles/forrent-imageprocessor:$1

    cp docker-compose-prod.yml docker-compose-prod-$1.yml

    sed -i '' -e "s/:tag/:$1/g" docker-compose-prod-$1.yml

    # we need enought free memory to run new containers without stop the olders
    # if there isn't enought memory, we have to stop the olders containers before deploy the newers
    ecs-cli compose --file docker-compose-prod-$1.yml service stop

    ecs-cli compose --file docker-compose-prod-$1.yml service up

    rm docker-compose-prod-$1.yml

fi
