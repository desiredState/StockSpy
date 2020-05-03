#!/usr/bin/env bash

set -e

function usage {
    cat <<EOF
usage: factory [-h] {build,test,buildtest,push} {client,server} ...

positional arguments:
  {build,test,push,all}
    build               build the Docker Image
    test {args}         run the container
    buildtest {args}    both of the above in that order
    push                push the Docker Image

  {client,server}
    client              operate on the client build
    server              operate on the server build

optional arguments:
  -h, --help            display this help message
EOF
}

function check_deps {
    DEPS=( 'docker' )

    for i in "${DEPS[@]}"; do
        if ! hash "${i}" 2>/dev/null; then
            echo -e "${RED}FACTORY > "${i}" is required. Please install it then try again.${NONE}"
            exit 1
        fi
    done
}

function build {
    echo -e "${MAGENTA}FACTORY > Building the ${NAMESPACE}/${IMAGE}:${TAG} Docker Image...${NONE}"
    docker build -f "${1}.Dockerfile" -t "${NAMESPACE}/${IMAGE}:${TAG}" .
    echo -e "${GREEN}FACTORY > OK.${NONE}"
}

function test {
    VERSION="${TAG}" UPDATE="${UPDATE}" ./wrapper.sh "${2}" "${@:3}"
}

function push {
    echo -e "${MAGENTA}FACTORY > Pushing the ${NAMESPACE}/${IMAGE}:${TAG} Docker Image...${NONE}"
    docker push "${NAMESPACE}/${IMAGE}:${TAG}"
    echo -e "${GREEN}FACTORY > OK.${NONE}"
}

#
# Entrypoint.
#

MAGENTA=$(tput setaf 5)
GREEN=$(tput setaf 2)
RED=$(tput setaf 1)
NONE=$(tput sgr 0)

check_deps

# Environment variable overrides.
export NAMESPACE=${NAMESPACE:='desiredstate'}
export TAG=${VERSION:='latest'}
export UPDATE=${UPDATE:=false}

case $2 in
    client)
        export IMAGE=${IMAGE:="stockspy-${2}"}
        ;;
    server)
        export IMAGE=${IMAGE:="stockspy-${2}"}
        ;;
    *)
        usage
        exit 1
esac

case $1 in
    build)
        build "${2}"
        ;;
    test)
        test "${@}"
        ;;
    buildtest)
        build "${2}"
        test "${@}"
        ;;
    push)
        push
        ;;
    *)
        usage
        exit 1
esac

echo -e "${GREEN}FACTORY > Finished.${NONE}"