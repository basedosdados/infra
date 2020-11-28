from google.cloud import tasks_v2
from google.protobuf import timestamp_pb2

# Create a client.
client = tasks_v2.CloudTasksClient()

# TODO(developer): Uncomment these lines and replace with your values.
project = 'basedosdados'
queue = "zip-full-table"
location = 'us-east1'
url = 'https://example.com/task_handler'
service_account_email = 'service-account@my-project-id.iam.gserviceaccount.com';
payload = 'hello'

# Construct the fully qualified queue name.
parent = client.queue_path(project, location, queue)

# Construct the request body.
task = {
    "http_request": {  # Specify the type of request.
        "http_method": tasks_v2.HttpMethod.POST,
        "url": url,  # The full url path that the task will be sent to.
        "oidc_token": {"service_account_email": service_account_email},
    }
}

if payload is not None:
    # The API expects a payload of type bytes.
    converted_payload = payload.encode()

    # Add the payload to the request.
    task["http_request"]["body"] = converted_payload

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
