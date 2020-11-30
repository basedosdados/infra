#!/bin/bash -e
http post https://zip-full-table-6op2ytwc6q-ue.a.run.app \
        "Authorization:Bearer $(gcloud auth print-identity-token)" \
        dataset=br_ms_sim table=municipio_causa_idade_genero_raca limit=45000
