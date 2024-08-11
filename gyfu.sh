#!/bin/bash

{
    read -r TAG
} <version.txt

NO_CACHE="false"
PUSH=""
#PUSH="--push"

# last one ends up on dockerhub
declare -a PLATFORMS=(
    "linux/arm64/v8"
    #    "linux/amd64"
)
for PLATFORM in "${PLATFORMS[@]}"; do
    BUILD_OPTIONS="--platform $PLATFORM $PUSH"
    if [ "$NO_CACHE" = true ]; then
        BUILD_OPTIONS+=" --no-cache=true"
        echo "building without cache"
    else
        echo "building with cache"
    fi
    docker buildx build $BUILD_OPTIONS -t josiahdc/shepherd:"${TAG}" ./shepherd
    docker buildx build $BUILD_OPTIONS -t josiahdc/polygon:"${TAG}" ./polygon
    docker buildx build $BUILD_OPTIONS -t josiahdc/liaison:"${TAG}" ./liaison
done
