terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.50.0"
    }
  }
}

resource "google_compute_network" "network" {
  name                    = var.campaign
  auto_create_subnetworks = false
  routing_mode            = "REGIONAL"
}

locals {
  compute_cidr_range = "10.33.0.0/16"
}

resource "google_compute_subnetwork" "compute" {
  name                     = "${var.campaign}-compute"
  ip_cidr_range            = local.compute_cidr_range
  network                  = google_compute_network.network.id
  private_ip_google_access = true
  region                   = var.region
}

resource "google_compute_firewall" "internal_traffic" {
  name          = "${var.campaign}-internal-traffic"
  network       = google_compute_network.network.name
  allow {
    protocol = "all"
  }
  source_ranges = [
    local.compute_cidr_range
  ]
}

resource "google_compute_firewall" "ssh_ingress" {
  name        = "${var.campaign}-ssh-ingress"
  network     = google_compute_network.network.name
  allow {
    protocol = "tcp"
    ports    = [
      "22"
    ]
  }
  target_tags = [
    "ssh-ingress"
  ]
  source_ranges = ["0.0.0.0/0"]
}

resource "google_compute_firewall" "trail" {
  name        = "${var.campaign}-trail"
  network     = google_compute_network.network.name
  allow {
    protocol = "tcp"
    ports    = [
      "33700",
      "33710"
    ]
  }
  target_tags = [
    "trail"
  ]
  source_ranges = ["0.0.0.0/0"]
}
