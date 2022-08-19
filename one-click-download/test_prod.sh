#!/bin/bash -e

DATASET=${1:-br_ms_sim}
TABLE=${2:-municipio_causa_idade_genero_raca}

http --timeout=300 post https://zip-full-table-6op2ytwc6q-ue.a.run.app \
        "Authorization:Bearer $(gcloud auth print-identity-token)" \
        dataset=$DATASET table=$TABLE limit=4500 debug=true

echo gs://basedosdados-public/test/one-click-download/$DATASET/$TABLE.zip
gsutil ls -l  gs://basedosdados-public/test/one-click-download/$DATASET/$TABLE.zip
