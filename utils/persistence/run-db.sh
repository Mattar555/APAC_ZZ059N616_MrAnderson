#!/bin/bash


# Complex

#podman run --name sales-db -p 5432:5432 -e POSTGRES_USER=salesuser -e POSTGRES_PASSWORD=salesuserpassword -e POSTGRES_DB=sales -v /Users/marwanattar/Documents/PTS/Agentic-AI-Hackathon/utils/persistence/init.complex.sql:/docker-entrypoint-initdb.d/init.sql -d postgres


# Simple

podman run --name sales-db -p 5432:5432 -e POSTGRES_USER=salesuser -e POSTGRES_PASSWORD=salesuserpassword -e POSTGRES_DB=sales -v /Users/marwanattar/Documents/PTS/Agentic-AI-Hackathon/utils/persistence/init.simple.sql:/docker-entrypoint-initdb.d/init.sql -d postgres



# podman exec -it sales-db psql -U salesuser -d sales
