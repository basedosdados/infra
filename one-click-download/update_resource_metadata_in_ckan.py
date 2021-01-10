#!/usr/bin/env python3

import os, json
from ckanapi import RemoteCKAN
import click

user_agent = None
CKAN_API_KEY = os.environ['CKAN_API_KEY']
CKAN_URL = os.environ.get('CKAN_URL', 'http://localhost:5000')

basedosdados = RemoteCKAN(CKAN_URL, user_agent=user_agent, apikey=CKAN_API_KEY)

@click.command()
@click.argument('package_name')
@click.argument('resource_name')
@click.argument('update_json', callback=lambda c, x: json.loads(x))
def update(package_name, resource_name, update_json):
    resource_id = get_resource_id(package_name, resource_name)

    resource = basedosdados.action.resource_show(id=resource_id)
    assert not set(update_json.keys()) - set(resource.keys())
    resource.update(update_json)
    updated_resource = basedosdados.action.resource_update(**resource)
    print('Resource successfully updated!')

def get_resource_id(package_name, resource_name):
    package = basedosdados.action.package_search(q=f'name:{package_name}')
    assert package['count'] == 1
    package = package['results'][0]
    assert package['name'] == package_name

    for p in package['resources']:
        if p['name'] == resource_name:
            return p['id']
    raise Exception(f'Resource {resource_name} not found')

if __name__ == "__main__":
    update()
