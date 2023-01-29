terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.50.0"
    }
  }
}

provider "google" {
  credentials = file(var.service_account_key_path)
  project     = var.project
  region      = var.region
  zone        = var.zone
}

provider "google-beta" {
  credentials = file(var.service_account_key_path)
  project     = var.project
  region      = var.region
  zone        = var.zone
}

module "network" {
  source   = "./modules/network"
  campaign = var.campaign
  region   = var.region
}

module "trail" {
  source            = "./modules/atlas"
  name              = "trail"
  service_name      = "${var.campaign}-trail"
  zone              = var.zone
  subnet            = module.network.compute_subnet
  disk_image_family = "atlas"
  instance_type     = "e2-small"
  private_ip        = "10.33.33.100"
  atlas_tags        = [
    "ssh-ingress",
    "trail"
  ]
}
