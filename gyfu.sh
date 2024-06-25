#!/bin/bash

NO_CACHE=true

declare -a PLATFORMS=(
    "linux/amd64"
    #     "linux/arm64/v8"
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
    docker buildx build "$NO_CACHE" --platform "$PLATFORM" -t josiahdc/trailhead:"${TAG}" --push ./trailhead
    docker buildx build "$NO_CACHE" --platform "$PLATFORM" -t josiahdc/switchback:"${TAG}" --push ./switchback
    docker buildx build "$NO_CACHE" --platform "$PLATFORM" -t josiahdc/zenith:"${TAG}" --push ./zenith
    docker buildx build "$NO_CACHE" --platform "$PLATFORM" -t josiahdc/cartographer:"${TAG}" --push --build-arg UNDERHILL_TAG="${TAG}" ./cartographer
    docker buildx build "$NO_CACHE" --platform "$PLATFORM" -t josiahdc/pathfinder:"${TAG}" --push ./pathfinder
done
