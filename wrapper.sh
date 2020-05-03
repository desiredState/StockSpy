#!/usr/bin/env bash

function usage {
    cat <<EOF
usage: stockspy [-h] {start,stop,logs} {client,server} ...

positional arguments:
  {start,stop,logs}
    start               start the container
    stop                stop the container
    logs                tail container logs

  {client,server}
    client              operate on the client
    server              operate on the server

optional arguments:
  -h, --help            display this help message
EOF
}

function check_deps {
    DEPS=( 'docker' )

    for i in "${DEPS[@]}"; do
        if ! hash "${i}" 2>/dev/null; then
            echo -e "${RED}StockSpy > "${i}" is required. Please install it then try again.${NONE}"
            exit 1
        fi
    done
}

function start {
}

function stop {
}

function logs {
}

MAGENTA=$(tput setaf 5)
GREEN=$(tput setaf 2)
RED=$(tput setaf 1)
NONE=$(tput sgr 0)

check_deps

NAMESPACE=${NAMESPACE:='desiredstate'}
TAG=${VERSION:='latest'}
UPDATE=${UPDATE:=false}

case $2 in
    client)
        IMAGE=${IMAGE:="stockspy-${2}"}
        ;;
    server)
        IMAGE=${IMAGE:="stockspy-${2}"}
        ;;
    *)
        usage
        exit 1
esac

case $1 in
    start)
        # TODO
        ;;
    stop)
        # TODO
        ;;
    logs)
        # TODO
        ;;
    *)
        usage
        exit 1
esac












case $1 in
    client)
        ARGS='-p 0.0.0.0:80:3000'
        ;;
    server)
        ARGS='-p 0.0.0.0:8080:5000'
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