#!/bin/bash
# Commit et push automatique avec un message générique
set -e

git add .
git commit -m "Trigger CI - Auto commit"
git push
