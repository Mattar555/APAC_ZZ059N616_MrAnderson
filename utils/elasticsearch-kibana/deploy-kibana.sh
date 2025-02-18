#!/bin/bash

# podman pull docker.elastic.co/kibana/kibana:8.17.2

podman run --network elastic --name kibana -e "ELASTICSEARCH_HOSTS=http://elastic:9200" -d -p 5601:5601 docker.elastic.co/kibana/kibana:8.17.2
