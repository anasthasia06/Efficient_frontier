#!/bin/bash
# Build l'image Docker sans cache
cd "$(dirname "$0")/.."
docker compose build --no-cache --dns=8.8.8.8
