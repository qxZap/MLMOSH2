#! /usr/bin/env bash

docker build --tag wumpus .
docker run -p 8000:8000 -it wumpus
