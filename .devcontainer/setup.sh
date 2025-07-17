#!/usr/bin/env bash
set -e

# Wait for gitpod bundle if running in Gitpod
if command -v gp &>/dev/null; then
    gp sync-await bundle
fi

pip install -r requirements.txt && pip install -r sidecar-requirements.txt

# Build Docker images used for local development

docker build . -f aeroalpes.Dockerfile -t aeroalpes/flask

docker build . -f adaptador.Dockerfile -t aeroalpes/adaptador
