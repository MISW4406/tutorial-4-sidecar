#!/usr/bin/env bash
set -e

pip install -r requirements.txt && pip install -r sidecar-requirements.txt

# Build Docker images used for local development

docker build . -f aeroalpes.Dockerfile -t aeroalpes/flask

docker build . -f adaptador.Dockerfile -t aeroalpes/adaptador
