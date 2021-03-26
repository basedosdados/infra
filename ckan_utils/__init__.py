import os, json, re
import functools
import stringcase
from ckanapi import RemoteCKAN

user_agent = None
CKAN_API_KEY = os.environ['CKAN_API_KEY']
CKAN_URL = os.environ.get('CKAN_URL', 'http://localhost:5000')

basedosdados = RemoteCKAN(CKAN_URL, user_agent=user_agent, apikey=CKAN_API_KEY)

@functools.lru_cache()
def get_dataset_name(d_id):
    return ckan.action.package_show(id=d_id)['name']

def update_resource_by_names(package_name, resource_name, update_dict):
    resource_id = get_resource_id(package_name, resource_name)
    update_resource(resource_id, update_dict)
    print(f'Resource {package_name}.{resource_name} successfully updated!')

def update_resource(resource_id, update_dict):
    resource = basedosdados.action.resource_show(id=resource_id)
    if non_existing := set(update_dict.keys()) - set([*resource.keys(), 'bdm_file_size']):
        raise Exception(f'Tried to add non-existing column(s): {non_existing}')
    resource.update(update_dict)
    updated_resource = basedosdados.action.resource_update(**resource)

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

def check_package_by_name(package_name):
    package_dict = basedosdados.action.package_show(id=package_name)
    updated_resource = basedosdados.action.package_update(**package_dict)
    print(f'Package {package_name} succesfully updated!')
