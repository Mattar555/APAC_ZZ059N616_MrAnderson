#!/bin/bash



# Pull

# podman pull docker.elastic.co/elasticsearch/elasticsearch:8.17.2

# Run - I have disabled security on purpose for this trivial demo

podman run --network elastic -d -e "discovery.type=single-node" -e "xpack.security.enabled=false" -e "xpack.security.enrollment.enabled=false" --name elastic  -p 9200:9200 -it -m 1GB docker.elastic.co/elasticsearch/elasticsearch:8.17.2

