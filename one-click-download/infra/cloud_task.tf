resource google_app_engine_application "basedosdados_app_engine" {
  location_id = "us-east1"
}

resource "google_cloud_tasks_queue" "zip_full_table" {
  name = "zip-full-table"
  location = "us-east1"
  retry_config {
    max_attempts = 3
    max_backoff = "30s"
    min_backoff = "3s"
  }

}

data "external" "docker_image" {
  program = ["bash", "-c", <<HERE
      docker images ${local.docker_image_name} --format '{"sha": "{{.Digest}}"}' | grep sha256 | head -1
      # echo '{"sha": "'$(docker images ${local.docker_image_name}:latest --digests --no-trunc -q)'"}'
HERE
  ]
}

resource "google_cloud_run_service" "zip_full_table_handler" {
  name     = "zip-full-table"
  location = "us-east1"

  metadata {
      annotations = {
          "run.googleapis.com/launch-stage" = "BETA"
      }
  }
  template {
    spec {
      service_account_name = google_service_account.task_role.email
      container_concurrency = 1
      containers {
        image = "${local.docker_image_name}@${data.external.docker_image.result.sha}"

        ports {
          container_port = 8080
        }
        resources {
            limits = {
                memory = "650Mi"
            }
        }
      }
      timeout_seconds = 3600
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}


resource "google_service_account" "task_role" {
  account_id   = "task-role"
  display_name = "A service account for async tasks"
}

# # This is bugged
# resource "google_service_account_iam_policy" "task_role_policy" {
#   service_account_id = google_service_account.task_role.name
#   policy_data        = data.google_iam_policy.task_role_policy.policy_data
# 
# }
# data "google_iam_policy" "task_role_policy" {
#   binding {
#       role = "roles/bigquery.admin"
#       role = "roles/storage.creator" # no public
#       members = [
#         "serviceAccount:${google_service_account.task_role.email}" # @basedosdados.iam.gserviceaccount.com"
#       ]
#   }
# }
