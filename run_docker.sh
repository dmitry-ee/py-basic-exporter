#!/bin/bash

container_name="wtbo"

docker rmi $(docker images | grep ${container_name} | awk '{ print $1 }')
docker run --rm \
  --name=${container_name} \
  --network=host \
  -e "LOG_LEVEL=INFO" \
  -e "WTBO_KAFKA_URL=localhost:9092" \
  -e "WTBO_SLEEP_MS=120000" \
  dmi7ry/${container_name}:latest
