#!/bin/bash
# Build l'image Docker sans cache
cd "$(dirname "$0")/.."
docker build --no-cache -t efficient_frontier:latest .
