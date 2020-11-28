#!/bin/bash -ex
DIR=`mktemp`
rm $DIR
mkdir $DIR
cd $DIR
trap "rm -rf $DIR" EXIT

mkfifo upload

gsutil rm -r 'gs://basedosdados-public/tmp/in/*' || true
bq query --nouse_legacy_sql <<'EOF'
    EXPORT DATA OPTIONS(
        uri='gs://basedosdados-public/tmp/in/file*.csv',
        format='CSV',
        overwrite=true,
        header=false,
        --compression='GZIP',
        field_delimiter=',')
    AS
    SELECT *
    FROM `basedosdados.br_ms_sim.municipio_causa_idade_genero_raca`
    LIMIT 100000
EOF

gsutil cp 'gs://basedosdados-public/tmp/in/*' - | gzip - | tee upload | wc --bytes > bytes_written &
gsutil cp upload gs://basedosdados-public/tmp/out
gsutil ls -l gs://basedosdados-public/tmp/out
wait
echo "Written $(cat bytes_written) bytes"
