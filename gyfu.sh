#!/bin/bash

NO_CACHE=false

declare -a PLATFORMS=(
    "linux/amd64"
    "linux/arm64/v8"
)
for PLATFORM in "${PLATFORMS[@]}"; do
    BUILD_OPTIONS="--platform $PLATFORM --push"
    if [ "$NO_CACHE" = true ]; then
        BUILD_OPTIONS+=" --no-cache=true"
        echo "building without cache"
    else
        echo "building with cache"
    fi

    {
        read -r TAG
    } <version.txt

    docker buildx build $BUILD_OPTIONS -t josiahdc/trailhead:"${TAG}" ./trailhead
    docker buildx build $BUILD_OPTIONS -t josiahdc/switchback:"${TAG}" ./switchback
    docker buildx build $BUILD_OPTIONS -t josiahdc/zenith:"${TAG}" ./zenith
    docker buildx build $BUILD_OPTIONS -t josiahdc/cartographer:"${TAG}" --build-arg UNDERHILL_TAG="${TAG}" ./cartographer
    docker buildx build $BUILD_OPTIONS -t josiahdc/pathfinder:"${TAG}" ./pathfinder
done
