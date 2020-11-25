provider "google" {
  project     = "basedosdados"
  region      = "us-east1"
}

terraform {
  backend "gcs" {
    bucket  = "basedosdados-pvt"
    prefix  = "terraform-states/one-click-download"
  }
}
