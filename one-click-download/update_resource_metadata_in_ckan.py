#!/usr/bin/env python3

import os, json, re
import stringcase
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
    return _update(package_name, resource_name, update_json)

def _update(package_name, resource_name, update_dict):
    resource_id = get_resource_id(package_name, resource_name)

    resource = basedosdados.action.resource_show(id=resource_id)
    assert not set(update_dict.keys()) - set([*resource.keys(), 'bdm_file_size'])
    resource.update(update_dict)
    updated_resource = basedosdados.action.resource_update(**resource)
    print(f'Resource {package_name}.{resource_name} successfully updated!')

def get_resource_id(package_name, resource_name):
    package_name = stringcase.spinalcase(package_name), stringcase.snakecase(package_name)
    package = basedosdados.action.package_search(q=f'name:{package_name[0]} || name:{package_name[1]}')
    assert package['count'] == 1, (package, package_name)
    package = package['results'][0]
    assert package['name'] in package_name, package

    for p in package['resources']:
        if re.search(rf'\b{resource_name}\b', p['name']):
            return p['id']
    raise Exception(f'Resource {resource_name} not found')

if __name__ == "__main__":
    update()
