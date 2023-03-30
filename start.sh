#!/bin/bash
export DATASTORE=redis
export BEARER_TOKEN="6449a78d-420d-4fa1-8c6e-5348bc5f73ba"
export OPENAI_API_KEY=${OPENAI_API_KEY}
export REDIS_HOST=localhost
export REDIS_PORT=6379
export REDIS_PASSWORD=${REDIS_PASSWORD}
poetry shell
poetry run start