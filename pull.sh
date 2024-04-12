#!/bin/bash

{
    read -r TAG
} <version.txt

docker pull josiahdc/trailhead:"${TAG}"
docker pull josiahdc/switchback:"${TAG}"
docker pull josiahdc/zenith:"${TAG}"
docker pull josiahdc/cartographer:"${TAG}"
docker pull josiahdc/pathfinder:"${TAG}"
