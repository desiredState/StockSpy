#!/usr/bin/env bash

docker rm -f $(docker ps -aq) && ./factory.sh buildtest -x -i 5 -u dannydirect90@gmail.com -p ybkdbblyhhjxjhav && git add -A && git commit -m 'Automation' && git push && git status && docker ps
