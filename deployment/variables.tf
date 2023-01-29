variable "service_account_key_path" {
  type    = string
  default = "~/clementinegroup/secrets/terraform_service_account.json"
}

variable "project" {
  type    = string
  default = "clementinegroup"
}

variable "region" {
  type    = string
  default = "us-west2"
}

variable "zone" {
  type    = string
  default = "us-west2-b"
}

variable "campaign" {
  type    = string
  default = "clementine"
}
