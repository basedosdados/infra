#!/bin/bash -e

docker-compose build && docker-compose push
cd infra; terraform apply -auto-approve; cd ..

docker run -it us-docker.pkg.dev/gcr-cleaner/gcr-cleaner/gcr-cleaner-cli \
        -token="$(gcloud auth print-access-token)" -repo us.gcr.io/basedosdados/zip_table -grace 30m
