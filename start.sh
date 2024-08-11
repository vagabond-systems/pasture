#!/bin/bash

{
    read -r TAG
} <version.txt

MAX_FLOCK_SIZE="5"
FLOCKMATE_IMAGE="josiahdc/polygon"
CREDS_DIRECTORY="$HOME/vagabond/secrets/pasture_test"
FLOCKMATE_ENVIRONMENT='{
    "BUCKET_NAME": "vagabond-pasture-test",
    "GCP_LOCATION": "us-east4",
    "MODEL_NAME": "gemini-1.5-pro-001",
    "PROJECT": "vagabondsystems",
    "GOOGLE_APPLICATION_CREDENTIALS": "/creds/key.json"
}'

docker stop pasture-shepherd >/dev/null 2>&1
docker rm pasture-shepherd >/dev/null 2>&1
docker run \
    --restart always \
    -d \
    --name pasture-shepherd \
    --network host \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -e VERSION_TAG="$TAG" \
    -e MAX_FLOCK_SIZE="$MAX_FLOCK_SIZE" \
    -e FLOCKMATE_IMAGE="$FLOCKMATE_IMAGE" \
    -e CREDS_DIRECTORY="$CREDS_DIRECTORY" \
    -e FLOCKMATE_ENVIRONMENT="$FLOCKMATE_ENVIRONMENT" \
    josiahdc/shepherd:"$TAG"
