#!/bin/bash

TAG=$(<../version.txt)

docker build --build-arg UNDERHILL_TAG="${TAG}" -t josiahdc/pathfinder:"${TAG}" .
