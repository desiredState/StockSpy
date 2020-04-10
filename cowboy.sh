#!/usr/bin/env bash

./factory.sh build && \
git add -A \
&& git commit -m 'Automation' && \
git push && \
git status; \
./factory.sh push
