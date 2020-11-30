#!/bin/bash -e

docker-compose build && docker-compose push
( cd infra; terraform apply -auto-approve) &
wait

#TODO add a cron in gcp to run gcr-clean
