#!/bin/bash -ex
DIR=`mktemp`
rm $DIR
mkdir $DIR
cd $DIR
trap "rm -rf $DIR" EXIT

DATASET=${1:?}
TABLE=${2:?}
LIMIT=${3}
if [[ $LIMIT ]]; then LIMIT="LIMIT ${LIMIT}"; fi


gsutil -m rm -r "gs://basedosdados-public/tmp/to_zip/$DATASET/$TABLE/" || true
bq query --nouse_legacy_sql <<EOF
    EXPORT DATA OPTIONS(
        uri="gs://basedosdados-public/tmp/to_zip/$DATASET/$TABLE/*.csv",
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

BLOB_PATH="one-click-download/$DATASET/$TABLE.zip" # todo add {version}
# FILE_NAME="${TABLE}.csv"
# mkfifo $FILE_NAME
mkfifo upload
mkfifo byte_count
mkfifo counter
gsutil cp "gs://basedosdados-public/tmp/to_zip/$DATASET/$TABLE/*" - | tee counter | gzip - | tee upload byte_count > /dev/null &
wc --bytes byte_count > bytes_written &
gsutil cp upload gs://basedosdados-public/$BLOB_PATH &
perl -nE 'say $. if ($. % 200000 == 0);' counter
gsutil ls -l gs://basedosdados-public/$BLOB_PATH
wait
echo "Written $(cat bytes_written) bytes"
