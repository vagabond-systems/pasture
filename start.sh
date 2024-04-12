#!/bin/bash

TAG=$(<version.txt)
docker run --rm --name underhill-cartographer --network host -v /var/run/docker.sock:/var/run/docker.sock josiahdc/cartographer:"${TAG}"
