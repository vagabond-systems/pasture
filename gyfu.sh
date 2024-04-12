#!/bin/bash

NO_CACHE=1

if [ $NO_CACHE -eq 1 ]; then
    NO_CACHE="--no-cache=true"
    echo "building without cache"
else
    NO_CACHE=""
    echo "building with cache"
fi

TAG=$(<version.txt)
echo "tag: $TAG"

# build image
docker buildx build $NO_CACHE --platform linux/amd64 -t josiahdc/trailhead:"${TAG}" ./trailhead --push
docker buildx build $NO_CACHE --platform linux/amd64 -t josiahdc/switchback:"${TAG}" ./switchback --push
docker buildx build $NO_CACHE --platform linux/amd64 -t josiahdc/zenith:"${TAG}" ./zenith --push
docker buildx build $NO_CACHE --platform linux/amd64 -t josiahdc/cartographer:"${TAG}" ./cartographer --push --build-arg UNDERHILL_TAG="${TAG}"
docker buildx build $NO_CACHE --platform linux/amd64 -t josiahdc/pathfinder:"${TAG}" ./pathfinder --push
