#!/usr/bin/env bash

IMAGE_NAME="${IMAGE_NAME:-kpn-api}"
HOST_PORT="${HOST_PORT:-8000}"
CONTAINER_PORT="${CONTAINER_PORT:-8000}"

echo "Starting Docker container from image: ${IMAGE_NAME}"
echo "Mapping host port ${HOST_PORT} to container port ${CONTAINER_PORT}"

docker run -p "${HOST_PORT}:${CONTAINER_PORT}" "${IMAGE_NAME}"