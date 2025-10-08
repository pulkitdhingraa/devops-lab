terraform {
  backend "s3" {
    bucket = "pd-simplewebapp-tf-state"
    key = "simplewebapp/terraform.tfstate"
    region = "ap-south-2"
    dynamodb_table = "tf-lock"
    encrypt = true
  }
}