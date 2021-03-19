#!/usr/bin/env python3
import flask
import sheets
import ckan_utils

app = flask.Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return flask.render_template('index.html')

@app.route('/', methods=['POST'])
def index_post():
    params = flask.request.form
    try:
        url = params['sheets_url']
        datasets, resources = sheets.get_datasets_and_resources(url)
        has_dataset = not datasets.empty
        return flask.render_template('index.html', **locals())
    except Exception as error:
        import traceback
        tb = traceback.format_exc()
        return flask.render_template('error.html', error=error, tb=tb)

@app.route('/update', methods=['POST'])
def index_post():
    params = flask.request.form
    try:
        url = params['sheets_url']
        datasets, resources = sheets.get_datasets_and_resources(url)
        has_dataset = not datasets.empty
        return flask.render_template('index.html', **locals())
    except Exception as error:
        import traceback
        tb = traceback.format_exc()
        return flask.render_template('error.html', error=error, tb=tb)

app.run(debug=True)
