terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "4.50.0"
    }
  }
}

resource "google_service_account" "atlas" {
  account_id = var.service_name
  display_name = var.service_name
}

resource "google_compute_instance_from_machine_image" "atlas" {
  provider = google-beta
  name     = var.name
  zone     = var.zone
  source_machine_image = "projects/clementinegroup/global/machineImages/atlas"
  machine_type = var.instance_type
  labels = {
    "service": var.service_name
  }
#  boot_disk {
#    auto_delete = true
#    initialize_params {
#      image = var.disk_image_family
#    }
#  }
  network_interface {
    subnetwork = var.subnet.name
    network_ip = var.private_ip
    access_config {}
  }
#  allow_stopping_for_update = true
  tags = var.atlas_tags
  service_account {
    email = google_service_account.atlas.email
    scopes = [
      "cloud-platform"
    ]
  }
}