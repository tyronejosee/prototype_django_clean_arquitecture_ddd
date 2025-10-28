variable "aws_access_key_id" {
  type      = string
  sensitive = true
}

variable "aws_secret_access_key" {
  type      = string
  sensitive = true
}

variable "paypal_client_id" {
  type      = string
  sensitive = true
}

variable "paypal_client_secret" {
  type      = string
  sensitive = true
}

variable "aws_region" {
  type    = string
  default = "us-east-2"
}

variable "project_name" {
  type    = string
  default = "marketly"
}

variable "image" {
  type = string
}

variable "container_port" {
  type    = number
  default = 8000
}

variable "db_username" {
  type    = string
  default = "grocery_user"
}

variable "db_password" {
  type      = string
  sensitive = true
}

variable "db_name" {
  type    = string
  default = "grocery_db"
}

variable "django_secret_key" {
  type      = string
  sensitive = true
}

variable "s3_bucket_name" {
  type    = string
  default = ""
}

variable "vpc_cidr" {
  type    = string
  default = "10.0.0.0/16"
}

variable "public_subnets" {
  type    = list(string)
  default = ["10.0.0.0/24", "10.0.1.0/24"]
}

variable "private_subnets" {
  type    = list(string)
  default = ["10.0.10.0/24", "10.0.11.0/24"]
}

variable "availability_zones" {
  type    = list(string)
  default = ["us-east-2a", "us-east-2b"]
}

variable "enable_cloudwatch_logs" {
  type    = bool
  default = true
}
