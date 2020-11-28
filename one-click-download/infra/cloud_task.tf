resource google_app_engine_application "basedosdados_app_engine" {
  location_id = "us-east1"
}

resource "google_cloud_tasks_queue" "zip_full_table" {
  name = "zip-full-table"
  location = "us-east1"
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
      containers {
        image = "us.gcr.io/basedosdados/test"
        # resources {
        #   
        # }
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

# resource "google_service_account_iam_policy" "task_role_policy" {
#   service_account_id = google_service_account.task_role.name
#   policy_data        = data.google_iam_policy.task_role_policy.policy_data
# 
# }
# data "google_iam_policy" "task_role_policy" {
#   binding {
#       role = "roles/run.invoker"
#       members = [
#         "serviceAccount:${google_service_account.task_role.email}"
#       ]
#   }
# }
