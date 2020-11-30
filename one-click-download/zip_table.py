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
    def __enter__(self): return self
    def __exit__(self, *_): self.file.close()

from contextlib import contextmanager

@contextmanager
def stream(file):
    gzip_file = gzip.GzipFile(fileobj=file, mode='w')
    try:
        str_to_bytes = encodings.utf_8.StreamWriter(gzip_file)
        try:
            csv_writer = csv.writer(str_to_bytes)
            yield csv_writer
        finally: str_to_bytes.close()
    finally: gzip_file.close()

def get_table_data(dataset, table, limit):
    limit = f"LIMIT {limit}" if limit else ''
    query = f"""
        SELECT *
        FROM `basedosdados.{dataset}.{table}`
        {limit}
    """
    query_job = BQ.query(query, )# max_results=100)
    return query_job.result()

def zip_full_table_and_store(dataset, table, limit=45000):

    table_data = get_table_data(dataset, table, limit)

    FIFO = f'/tmp/{dataset}--{table}--{datetime.now().replace(microsecond=0).isoformat()}.csv'
    os.mkfifo(FIFO)

    print('spawn uploader')
    blob_path = f'one-click-download/{dataset}/{table}.zip' # todo add {version}
    process = subprocess.Popen(f'gsutil cp - gs://{BUCKET}/{blob_path} < {FIFO}', shell=True) # streaming not suported nativelly on py
    assert process.poll() is None


    with FileWithCounter(FIFO, 'wb') as fifo, stream(fifo.file) as csv_writer:
        for idx, line in enumerate(table_data):
            csv_writer.writerow(line.values())
            if idx % 200_000 == 0: print(idx)

    print('Foi')
    assert process.wait(10) == 0, process.poll()
    os.unlink(FIFO)
    output = f'wrote {boltons.strutils.bytes2human(fifo.written_bytes)} ({fifo.written_bytes}B) on gs://{BUCKET}/{blob_path}'
    size_on_bucket = subprocess.run(f"gsutil ls -l gs://{BUCKET}/{blob_path}".split(), capture_output=True, encoding='utf8')
    size_on_bucket = int(size_on_bucket.stdout.split()[0])
    assert size_on_bucket == fifo.written_bytes
    print(output)
    return output

if __name__ == '__main__': main()
