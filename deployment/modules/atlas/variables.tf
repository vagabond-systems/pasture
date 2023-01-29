variable "service_name" {
  type = string
}

variable "name" {
  type = string
}

variable "zone" {
  type = string
}

variable "subnet" {
  type = object({
    name = string
  })
}

variable "disk_image_family" {
  type = string
}

variable "instance_type" {
  type = string
}

variable "private_ip" {
  type = string
}

variable "atlas_tags" {
  type = list(string)
}

