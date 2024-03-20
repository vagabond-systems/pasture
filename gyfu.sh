#!/bin/bash

TAG="0.35"

# build image
docker buildx build --platform linux/amd64 -t josiahdc/trailhead:${TAG} ./trailhead --push
docker buildx build --platform linux/amd64 -t josiahdc/switchback:${TAG} ./switchback --push
docker buildx build --platform linux/amd64 -t josiahdc/zenith:${TAG} ./zenith --push
