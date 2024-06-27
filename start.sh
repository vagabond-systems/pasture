#!/bin/bash

{
    read -r TAG
} <version.txt
{
    read -r VPN_USERNAME
    read -r VPN_PASSWORD
} <creds.txt
docker stop underhill-cartographer > /dev/null 2>&1
docker rm underhill-cartographer > /dev/null 2>&1
docker run \
    --restart always \
    -d \
    --name underhill-cartographer \
    -e TRAIL_COUNT=5 \
    -e VPN_USERNAME="$VPN_USERNAME" \
    -e VPN_PASSWORD="$VPN_PASSWORD" \
    --network host -v /var/run/docker.sock:/var/run/docker.sock \
    josiahdc/cartographer:"${TAG}"
