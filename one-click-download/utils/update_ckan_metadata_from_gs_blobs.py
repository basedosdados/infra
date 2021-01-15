#!/usr/bin/env python3

from concurrent.futures import ThreadPoolExecutor
from google.cloud import storage
from update_resource_metadata_in_ckan import basedosdados as ckan, _update as update_resource
from stringcase import snakecase, spinalcase
import functools


gs = storage.Client()
bucket = gs.get_bucket("basedosdados-public")

def get_size_and_update(dataset, table):
    blob = bucket.blob(f'one-click-download/{snakecase(dataset)}/{snakecase(table)}.zip')
    if blob.exists():
        blob.reload()
        size = blob.size
        assert size > 1
    else:
        size = 'Unavailable'
    print(f'setting size to {size} @ {dataset}.{table}')
    update_resource(dataset, table, {'bdm_file_size': size})
    return True

@functools.lru_cache()
def get_dataset_name(d_id):
    return ckan.action.package_show(id=d_id)['name']


resources_to_update = ckan.action.resource_search(query='is_bdm:BD+')
assert resources_to_update['count'] == len(resources_to_update['results'])
resources_to_update = resources_to_update['results']
resources_to_update = [
        {'dataset': get_dataset_name(r['package_id']), 'table': r['name']}
        for r in resources_to_update
        if '["BD+"]' in r['is_bdm']  # ckan search in extras is a bit buggy
]

pool = ThreadPoolExecutor(20)
assert all(pool.map(lambda x: get_size_and_update(**x), resources_to_update))
