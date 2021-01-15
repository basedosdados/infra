#!/bin/bash -e

http --timeout=300 post https://zip-full-table-6op2ytwc6q-ue.a.run.app \
        "Authorization:Bearer $(gcloud auth print-identity-token)" \
        dataset=br_ms_sim table=municipio_causa_idade_genero_raca limit=4500 debug=true

echo gs://basedosdados-public/test/one-click-download/br_ms_sim/municipio_causa_idade_genero_raca.zip
gsutil ls -l  gs://basedosdados-public/test/one-click-download/br_ms_sim/municipio_causa_idade_genero_raca.zip
