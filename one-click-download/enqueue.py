#!/usr/bin/env python3
from google.cloud import tasks_v2
from google.protobuf import timestamp_pb2, duration_pb2
import json

# Create a client.
client = tasks_v2.CloudTasksClient()

project = 'basedosdados'
queue = "zip-full-table"
location = 'us-east1'
url = 'https://zip-full-table-6op2ytwc6q-ue.a.run.app'
# url = 'https://endwng7ki4wtl.x.pipedream.net'
service_account_email = 'task-role@basedosdados.iam.gserviceaccount.com'
payload = dict(dataset='br_ms_sim', table='municipio_causa_idade_genero_raca', limit=None)
in_seconds = None
task_name = None

# Construct the fully qualified queue name.
parent = client.queue_path(project, location, queue)

# Construct the request body.
task = {
    "http_request": {  # Specify the type of request.
        "http_method": tasks_v2.HttpMethod.POST,
        "url": url,
        "oidc_token": {"service_account_email": service_account_email},
    }
    ,"dispatch_deadline": duration_pb2.Duration(seconds=60*30) # 30m is maximum :/
}

if payload is not None:
    # The API expects a payload of type bytes.
    converted_payload = json.dumps(payload).encode()

    # Add the payload to the request.
    task["http_request"]["body"] = converted_payload
    task["http_request"]["headers"] = {"Content-type": "application/json"}


if in_seconds is not None:
    # Convert "seconds from now" into an rfc3339 datetime string.
    d = datetime.datetime.utcnow() + datetime.timedelta(seconds=in_seconds)

    # Create Timestamp protobuf.
    timestamp = timestamp_pb2.Timestamp()
    timestamp.FromDatetime(d)

    # Add the timestamp to the tasks.
    task["schedule_time"] = timestamp

if task_name is not None:
    # Add the name to tasks.
    task["name"] = task_name

# Use the client to build and send the task.
response = client.create_task(request={"parent": parent, "task": task})

print("Created task {}".format(response.name))
print(response)
