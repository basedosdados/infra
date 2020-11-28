#!/usr/bin/env python3
from functools import partial
from sys import argv
import os, csv, encodings, subprocess, gzip
import time
from datetime import datetime
import boltons.strutils

from google.cloud import bigquery
from google.cloud import storage
from google.cloud.storage.blob import Blob
from google.cloud.storage.bucket import Bucket

BQ = bigquery.Client()
# CS = storage.Client()
# bucket = Bucket(CS, name='basedosdados-public')
# blob = bucket.Blob(name='tmp/test')
BUCKET = 'basedosdados-public'

def main():
    zip_full_table_and_store(argv[1], argv[2], argv[3] if len(argv) > 3 else None)

class FileWithCounter:
    def __init__(self, *a):
        self.file =  open(*a)
        self.written_bytes = 0
        def write(data):
            self.written_bytes += self.file.old_write(data)
        self.file.old_write, self.file.write = self.file.write, write

def zip_full_table_and_store(dataset, table, limit=45000):
    limit = f"LIMIT {limit}" if limit else ''
    query = f"""
        SELECT *
        FROM `basedosdados.{dataset}.{table}`
        {limit}
    """
    query_job = BQ.query(query, )# max_results=100)

    FIFO = f'/tmp/zip-fifo-{datetime.now().timestamp()}'
    try: os.mkfifo(FIFO)
    except FileExistsError: pass

    print('spawn uploader')
    blob_path = 'tmp/test'
    process = subprocess.Popen(f'gsutil cp - gs://{BUCKET}/{blob_path} < {FIFO}', shell=True) # streaming not suported nativelly on py
    assert process.poll() is None

    fifo = FileWithCounter(FIFO, 'wb')

    gzip_file = gzip.GzipFile(fileobj=fifo.file, mode='w')
    str_to_bytes = encodings.utf_8.StreamWriter(gzip_file)
    csv_writer = csv.writer(str_to_bytes)

    for idx, line in enumerate(query_job.result()):
        csv_writer.writerow(line.values())
        if idx % 10000 == 0: print(idx)

    str_to_bytes.close()
    gzip_file.close()
    fifo.file.close()

    print('Foi')
    assert process.wait(10) == 0
    output = f'wrote {boltons.strutils.bytes2human(fifo.written_bytes)} ({fifo.written_bytes}B)'
    size_on_bucket = subprocess.run("gsutil ls -l gs://basedosdados-public/tmp/test".split(), capture_output=True, encoding='utf8')
    size_on_bucket = int(size_on_bucket.stdout.split()[0])
    assert size_on_bucket == fifo.written_bytes
    print(output)
    return output



if __name__ == '__main__': main()

def test_main():
    dataset = 'br_ms_sim'
    table = 'municipio_causa_idade_genero_raca'
    zip_full_table_and_store(dataset, table)
