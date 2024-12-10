terraform {
  backend "s3" {
    bucket         = "terraform-state-bucket"  # The name of the S3 bucket
    key            = "terraform/state/terraform.tfstate"
    region         = "'us-east-1"  # Ensure this matches the region of your bucket
    dynamodb_table = "terraform-lock-table"  # DynamoDB table for state locking
    encrypt        = true
  }
}
