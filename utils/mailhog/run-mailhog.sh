#!/bin/bash


podman run --name mailserver -d -p 8025:8025 -p 1025:1025 mailhog/mailhog


