terraform {
  backend "s3" {
    bucket         = "terraform-state-bucket"  # Replace with your S3 bucket name
    key            = "terraform/state/terraform.tfstate"
    region         = "ap-south-1"  # Your AWS region
    dynamodb_table = "terraform-lock-table"  # DynamoDB table for state locking
    encrypt        = true  # Encrypt the state file in S3
  }
}
