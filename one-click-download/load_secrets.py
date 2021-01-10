from google.cloud import secretmanager
import os, json

_client = secretmanager.SecretManagerServiceClient()

def load_secret_from_env():
    for s in json.loads(os.environ.get('SECRETS', '[]')):
        load_secret(s)

def load_secret(secret_id):
    response = _client.access_secret_version(request={"name": secret_id})
    payload = response.payload.data.decode("UTF-8")
    os.environ.update(json.loads(payload))
