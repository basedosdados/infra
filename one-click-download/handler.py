#!/usr/bin/env python3
import bottle
from zip_table import zip_full_table_and_store
import json, subprocess
import load_secrets
load_secrets.load_secret_from_env()

app = bottle.Bottle()

@app.route('/', method='POST')
def zip_bash():
    body = bottle.request.json
    args = ['/app/bash_zip_table.sh', body['dataset'], body['table'],]
    if body.get('limit'): args.append(body['limit'])
    if body.get('debug'): args.append(str(body['debug']))
    output = subprocess.run(args, capture_output=False, encoding='utf8', check=True)
    return {'output': 'ok'}

@app.error()
def error(e):
    bottle.response.status = e.status_code
    bottle.response.set_header('Content-Type', 'application/json')
    bottle.response.body = json.dumps({'error': e.traceback, 'code': e.status_code})
    return bottle.response

bottle.run(app, host='0.0.0.0', port=8080)
