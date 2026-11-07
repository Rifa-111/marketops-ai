terraform {
  required_version = ">= 1.6.0"
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 5.0" }
  }
}
variable "aws_region" { type = string; default = "eu-west-2" }
variable "bucket_name" { type = string }
provider "aws" { region = var.aws_region }
resource "aws_s3_bucket" "raw_trades" { bucket = var.bucket_name }
resource "aws_s3_bucket_public_access_block" "raw_trades" {
  bucket = aws_s3_bucket.raw_trades.id
  block_public_acls = true
  block_public_policy = true
  ignore_public_acls = true
  restrict_public_buckets = true
}
resource "aws_s3_bucket_versioning" "raw_trades" {
  bucket = aws_s3_bucket.raw_trades.id
  versioning_configuration { status = "Enabled" }
}
resource "aws_s3_bucket_server_side_encryption_configuration" "raw_trades" {
  bucket = aws_s3_bucket.raw_trades.id
  rule { apply_server_side_encryption_by_default { sse_algorithm = "AES256" } }
}
output "raw_bucket" { value = aws_s3_bucket.raw_trades.id }
