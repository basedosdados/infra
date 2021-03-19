# https://discuss.streamlit.io/t/how-to-use-streamlit-with-nginx/378/13
import ckan_utils
import pandas as pd
import streamlit as st
import sheets
w = st.write


def main():
    st.title('Google Sheets -> Base dos Dados updater')
    w('Please insert google sheets url to be updated')
    url = st.text_input('sheets_url')
    if not url: st.stop()

    datasets, resources = sheets.get_datasets_and_resources(url)
    st.subheader('Datasets and Resources found:')
    w('Datasets'); w(datasets)
    w('Resources'); w(resources)

    datasets_diffs = {}
    # datasets_diffs = {resource['name']: diff for resource in resources.to_dict('records') if not (diff := _get_dataset_diff(resource)).empty}
    resources_diffs = {resource['name']: diff for resource in resources.to_dict('records') if not (diff := _get_resource_diff(resource)).empty}
    if datasets_diffs or resources_diffs:
        st.subheader('Changes detected:')
        for dataset_name, diff in datasets_diffs.items():
            w(f"Dataset: {resource_name!r}")
            w(diff)
        for resource_name, diff in resources_diffs.items():
            w(f"Resource: {resource_name!r}")
            w(diff)
    else:
        st.subheader('No changes detected.')
        st.stop()

    update = st.button('Update datasets and resources')
    if not update: st.stop()
    do_update(datasets, resources)
    w('Datasets and Resources successfully updated. Please reload!')
    st.button('Reload')


def do_update(datasets, resources):
    for resource in resources.to_dict('records'):
        try:
            resource_id = resource['id']
            resource_at_ckan = ckan_utils.basedosdados.action.resource_show(id=resource_id)
            ckan_utils.update_resource(resource_id, resource)
        except Exception as e:
            st.error(f'Resource: {resource["id"]!r} failed to update. Debugging info bellow.')
            st.error(f'resource at google sheets: {resource}')
            if locals().get('resource_at_ckan'):
                st.error(f'resource at ckan: {resource_at_ckan}')
            raise

def _get_dataset_diff(dataset):
    dataset_at_ckan = ckan_utils.basedosdados.action.package_show(id=dataset['id'])
    return _get_x_diff(dataset, dataset_at_ckan)

def _get_resource_diff(resource):
    resource_at_ckan = ckan_utils.basedosdados.action.resource_show(id=resource['id'])
    return _get_x_diff(resource, resource_at_ckan)

def _get_x_diff(x, x_at_ckan):
    x_at_ckan_altered_keys = pd.Series({k:v for k, v in x_at_ckan.items() if k in x})
    diff = x_at_ckan_altered_keys.sort_index().compare(pd.Series(x).sort_index())
    diff = diff.rename(columns={'other': 'at base dos dados', 'self': 'at google sheets'})
    return diff

if __name__ == '__main__': main()
