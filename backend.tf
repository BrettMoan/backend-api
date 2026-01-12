terraform {
  backend "s3" {
    bucket = "brettmoan-qa-tfstate-a5d103ec"
    key = "backend-api/terraform.tfstate"
    region = "us-east-1" # or your region
  }

  required_version = ">= 1.14.3"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}
