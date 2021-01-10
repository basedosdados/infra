#!/bin/bash -ex
DIR=`mktemp`
rm $DIR
mkdir $DIR
cd $DIR
trap "rm -rf $DIR" EXIT

DATASET=${1:?}
TABLE=${2:?}
LIMIT=${3}
DEBUG=${4}
if [[ $DEBUG ]]; then DEBUG="test/"; fi
if [[ $LIMIT ]]; then LIMIT="LIMIT ${LIMIT}"; fi

BLOB_PATH="basedosdados-public/${DEBUG}one-click-download/$DATASET/$TABLE.zip" # todo add {version}
SCRATCH_PATH="basedosdados-public/${DEBUG}tmp/to_zip/$DATASET/$TABLE"

gsutil -m rm -r "gs://$SCRATCH_PATH" || true
trap "gsutil -m rm -r 'gs://$SCRATCH_PATH' || true" EXIT

bq query --nouse_legacy_sql --format=csv "SELECT * FROM \`basedosdados.$DATASET.$TABLE\` LIMIT 1" | head -1 > headers # field names cant have newlines, bq forbids it
bq query --nouse_legacy_sql --allow_large_results <<EOF
    EXPORT DATA OPTIONS(
        uri="gs://$SCRATCH_PATH/*.csv",
        format='CSV',
        overwrite=true,
        header=false,
        --compression='GZIP',
        field_delimiter=',')
    AS
    SELECT *
    FROM \`basedosdados.$DATASET.$TABLE\`
    $LIMIT
EOF

FILE_NAME="${TABLE}.csv"
mkfifo $FILE_NAME upload byte_count counter
( cat headers ; gsutil cp "gs://$SCRATCH_PATH/*" - ) | tee counter > $FILE_NAME & PIDS="$PIDS $!"
zip --fifo -6 - $FILE_NAME | tee upload > byte_count & PIDS="$PIDS $!"
wc --bytes byte_count > bytes_written & PIDS="$PIDS $!"
gsutil cp - gs://$BLOB_PATH < upload & PIDS="$PIDS $!"
perl -nE 'say $. if ($. % 200000 == 0);' < counter & PIDS="$PIDS $!"
trap "kill $PIDS 2> /dev/null || true" EXIT
sleep 1 && kill -0 $PIDS # Abort if any sub process is dead
for p in $PIDS; do wait -n ; done
gsutil ls -l gs://$BLOB_PATH
echo "Written $(cat bytes_written) bytes"
./update_resource_metadata_in_ckan.py $DATASET $TABLE '{"bdm_file_size": '"$(cat bytes_written)"'}'
echo Done
