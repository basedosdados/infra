#!/usr/bin/env python3
import bottle
from zip_table import zip_full_table_and_store
import json

app = bottle.Bottle()

@app.route('/', method='POST')
def hello():
    args = bottle.request.json
    output = zip_full_table_and_store(args['dataset'], args['table'], args.get('limit'))
    return {'output': output}

@app.error()
def error(e):
    bottle.response.status = e.status_code
    bottle.response.set_header('Content-Type', 'application/json')
    bottle.response.body = json.dumps({'error': e.traceback, 'code': e.status_code})
    return bottle.response

bottle.run(app, host='0.0.0.0', port=8080)
