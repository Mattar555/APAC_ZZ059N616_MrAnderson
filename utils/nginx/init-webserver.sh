#!/bin/bash


podman run -it --rm -d -p 8080:80 --name web -v /Users/marwanattar/Documents/PTS/Agentic-AI-Hackathon/utils/nginx/site-content:/usr/share/nginx/html nginx
