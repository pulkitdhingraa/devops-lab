variable "vpc_cidr" {
  type = string
}

variable "public_cidr" {
  type = list(string)
}

variable "private_cidr" {
  type = string
}

variable "ami" {
  type = string
}

variable "userdatafile" {
  type = string
}