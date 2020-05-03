#!/usr/bin/env bash

if ! hash docker &>/dev/null; then
    echo 'Docker is required to run StockSpy. Please install it then try again.'
    exit 1
fi

case $1 in
    client)
        ARGS=${ARGS:='-p 0.0.0.0:80:3000'}
        ;;
    server)
        ARGS=${ARGS:='-p 0.0.0.0:8080:5000'}
        ;;
    *)
        echo 'Usage: stockspy {client,server} [args]'
        exit 1
esac

NAMESPACE=${NAMESPACE:='desiredstate'}
IMAGE=${IMAGE:="stockspy-${1}"}
TAG=${VERSION:='latest'}
UPDATE=${UPDATE:=true}

echo 'StockSpy > Updating...'
if [[ $UPDATE = true ]] ; then
    docker pull "${NAMESPACE}/${IMAGE}:${TAG}" > /dev/null
fi

echo 'StockSpy > Removing old version...'
docker rm -f "stockspy-${1}" &> /dev/null

echo 'StockSpy > Starting...'
docker run --name "stockspy-${1}" \
           -d \
           --restart always \
           ${ARGS} \
           "${NAMESPACE}/${IMAGE}:${TAG}" ${@:2} \
           > /dev/null

echo 'StockSpy > Cleaning up...'
docker system prune -f > /dev/null

echo "StockSpy > Done! Use \"docker logs -f stockspy-${1}\" to tail logs."