#!/usr/bin/env bash

if ! hash docker &>/dev/null; then
    echo 'Docker is required to run StockSpy. Please install it then try again.'
    exit 1
fi

NAMESPACE=${NAMESPACE:='desiredstate'}
TAG=${VERSION:='latest'}
UPDATE=${UPDATE:=true}

case $1 in
    client)
        export IMAGE=${IMAGE:="stockspy-${1}"}
        export ARGS='-p=0.0.0.0:80:3000'
        ;;
    server)
        export IMAGE=${IMAGE:="stockspy-${1}"}
        export ARGS='-p=0.0.0.0:8080:5000'
        ;;
    *)
        echo 'Usage: stockspy {client,server}'
        exit 1
esac

echo 'StockSpy > Updating...'
if [[ "$UPDATE" = true ]] ; then
    docker pull "${NAMESPACE}/${IMAGE}:${TAG}" > /dev/null
fi

echo 'StockSpy > Removing old version...'
docker rm -f "stockspy-${1}" > /dev/null

echo 'StockSpy > Starting...'
docker run --name "stockspy-${1}" \
           -d \
           --restart always \
           "${ARGS}" \
           "${NAMESPACE}/${IMAGE}:${TAG}" "${@}" \
           > /dev/null

echo 'StockSpy > Cleaning up...'
docker system prune -f > /dev/null

echo "StockSpy > Done! Use \"docker logs -f stockspy-${1}\" to tail logs."