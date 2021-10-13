#!/bin/bash

docker build -t dockwork-client -f ./docker/Dockerfile .

docker tag dockwork-client disi33/dockwork-client:latest
docker push disi33/dockwork-client:latest