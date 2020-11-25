resource google_app_engine_application "basedosdados_app_engine" {
  location_id = "us-east1"
}

resource "google_cloud_tasks_queue" "zip_full_table" {
  name = "zip-full-table"
  location = "us-east1"
}
