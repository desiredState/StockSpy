#!/usr/bin/env bash

NAMESPACE=${NAMESPACE:='desiredstate'}
IMAGE=${IMAGE:='stockspy'}
TAG=${VERSION:='latest'}
UPDATE=${UPDATE:=true}

if ! hash docker &>/dev/null; then
    echo 'Docker is required to run StockSpy. Please install it then try again.'
    exit 1
fi

echo 'StockSpy > Updating...'
if [[ "$UPDATE" = true ]] ; then
    docker pull "${NAMESPACE}/${IMAGE}:${TAG}" > /dev/null
fi

echo 'StockSpy > Removing old version...'
docker rm -f stockspy > /dev/null

echo 'StockSpy > Starting...'
docker run --name stockspy \
           -d \
           --restart always \
           -p 0.0.0.0:8080:5000 \
           -p 0.0.0.0:80:3000 \
           "${NAMESPACE}/${IMAGE}:${TAG}" "${@}" \
           > /dev/null

echo 'StockSpy > Cleaning up...'
docker system prune -f > /dev/null

echo 'StockSpy > Done! Use "docker logs -f stockspy" to tail logs.'