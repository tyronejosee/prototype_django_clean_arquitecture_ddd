resource "aws_s3_bucket" "app_bucket" {
  bucket = length(var.s3_bucket_name) > 0 ? var.s3_bucket_name : "${var.project_name}-bucket-${random_id.suffix.hex}"
  # acl           = "private"
  force_destroy = true # TODO: review this
  tags          = { Name = "${var.project_name}-bucket" }
}

resource "aws_s3_bucket_public_access_block" "app_bucket_block" {
  bucket                  = aws_s3_bucket.app_bucket.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
