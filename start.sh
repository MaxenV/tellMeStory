#!/bin/bash

source environment/.env

if [ "$GPU_AVAILABLE" = "TRUE" ]; then
  docker compose -f "./environment/docker-compose.yml" up -d ollama-gpu django-tell-me-story
else
  docker compose -f "./environment/docker-compose.yml" up -d ollama-no-gpu django-tell-me-story
fi