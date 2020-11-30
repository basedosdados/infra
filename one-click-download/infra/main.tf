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

terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
    }
  }
  required_version = ">= 0.13"
}

locals {
  docker_image_name = "us.gcr.io/basedosdados/zip_table"
}
