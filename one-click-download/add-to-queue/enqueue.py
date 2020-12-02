#!/usr/bin/env python3
from google.cloud import tasks_v2
from google.oauth2 import service_account
from google.protobuf import timestamp_pb2, duration_pb2
import json
from pathlib import Path


def add_to_queue(
    client,
    dataset,
    table,
    limit,
    project="basedosdados",
    queue="zip-full-table",
    location="us-east1",
    url="https://zip-full-table-6op2ytwc6q-ue.a.run.app",
    service_account_email="task-caller@basedosdados.iam.gserviceaccount.com",
    in_seconds=None,
    task_name=None,
):

    payload = dict(dataset=dataset, table=table, limit=None)

    # Construct the fully qualified queue name.
    parent = client.queue_path(project, location, queue)

    # Construct the request body.
    task = {
        "http_request": {  # Specify the type of request.
            "http_method": tasks_v2.HttpMethod.POST,
            "url": url,
            "oidc_token": {"service_account_email": service_account_email},
        },
        "dispatch_deadline": duration_pb2.Duration(
            seconds=60 * 30
        ),  # 30m is maximum :/
        # "name": f"{dataset}-{table}",
    }

    if payload is not None:
        # The API expects a payload of type bytes.
        converted_payload = json.dumps(payload).encode()

        # Add the payload to the request.
        task["http_request"]["body"] = converted_payload
        task["http_request"]["headers"] = {"Content-type": "application/json"}

    # Use the client to build and send the task.
    response = client.create_task(request={"parent": parent, "task": task})

    print("Created task {}".format(response.name))
    print(response)


def main(main_project_path, credentials_path, runall=False):

    # Create a client.
    credentials = service_account.Credentials.from_service_account_file(
        credentials_path
    )
    client = tasks_v2.CloudTasksClient(credentials=credentials)

    if runall:
        p = Path(main_project_path)
        for f in (p / "bases").glob("*/*"):
            dataset, table = str(f).split("/")[-2:]

            if table not in ("README.md", "code"):
                print(dataset, table)

    add_to_queue(client, dataset="br_inep_ideb", table="regiao", limit=100)


if __name__ == "__main__":

    main(
        main_project_path # Path with all metadata
        credentials_path  # Path with gcloud service account json credential file
        runall            # Boolean to run all datasets and tables
    )