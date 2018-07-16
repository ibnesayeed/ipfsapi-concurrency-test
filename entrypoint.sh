#!/usr/bin/env bash

set -e

# Run the IPFS daemon in background
ipfs daemon &

# Wait for IPFS daemon to be ready
while ! curl -s localhost:5001 > /dev/null
do
    sleep 1
done

exec "$@"
