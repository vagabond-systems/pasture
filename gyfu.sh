#!/bin/bash

NO_CACHE=false

declare -a PLATFORMS=(
     "linux/amd64"
     "linux/arm64/v8"
)

if [ "$NO_CACHE" = true ]; then
    NO_CACHE="--no-cache=true"
    echo "building without cache"
else
    NO_CACHE=""
    echo "building with cache"
fi

{
    read -r TAG
} <version.txt

for PLATFORM in "${PLATFORMS[@]}"; do
    docker buildx build $NO_CACHE --platform $PLATFORM -t josiahdc/trailhead:"${TAG}" ./trailhead --push
    docker buildx build $NO_CACHE --platform $PLATFORM -t josiahdc/switchback:"${TAG}" ./switchback --push
    docker buildx build $NO_CACHE --platform $PLATFORM -t josiahdc/zenith:"${TAG}" ./zenith --push
    docker buildx build $NO_CACHE --platform $PLATFORM -t josiahdc/cartographer:"${TAG}" ./cartographer --push --build-arg UNDERHILL_TAG="${TAG}"
    docker buildx build $NO_CACHE --platform $PLATFORM -t josiahdc/pathfinder:"${TAG}" ./pathfinder --push
done