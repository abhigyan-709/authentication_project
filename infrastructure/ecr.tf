# Provider Configuration
provider "aws" {
  region = "ap-south-1" # Change to your desired region
}

# ECR Repository
resource "aws_ecr_repository" "auth_repo" {
  name = "auth_app_repo"

  image_scanning_configuration {
    scan_on_push = true
  }

  image_tag_mutability = "MUTABLE"
}

# Output the Repository URL
output "repository_url" {
  value = aws_ecr_repository.auth_repo.repository_url
}

# IAM Policy for ECR Access
resource "aws_iam_policy" "ecr_policy" {
  name        = "ECRAccessPolicy"
  description = "Policy to allow access to ECR resources"
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = [
          "ecr:*",           # All ECR actions
          "iam:GetUser",     # Get IAM user information
          "sts:AssumeRole"   # Assume roles
        ],
        Effect   = "Allow",
        Resource = "*"
      }
    ]
  })
}

# IAM User
resource "aws_iam_user" "ecr_user" {
  name = "ecr_user"
}

# Attach the Policy to the IAM User
resource "aws_iam_user_policy_attachment" "ecr_policy_attachment" {
  user       = aws_iam_user.ecr_user.name
  policy_arn = aws_iam_policy.ecr_policy.arn
}

# (Optional) IAM Role for Role Assumption
resource "aws_iam_role" "ecr_role" {
  name = "ECRRole"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = {
          Service = "ec2.amazonaws.com" # Update based on the service or user assuming the role
        },
        Action = "sts:AssumeRole"
      }
    ]
  })
}

# Attach the Policy to the Role
resource "aws_iam_role_policy_attachment" "ecr_role_policy_attachment" {
  role       = aws_iam_role.ecr_role.name
  policy_arn = aws_iam_policy.ecr_policy.arn
}

# S3 Bucket for Terraform State
resource "aws_s3_bucket" "terraform_state_bucket" {
  bucket = "terraform-state-bucket"  # Use a globally unique name for your bucket
  region = "'us-east-1"  # Change to your desired region

  versioning {
    enabled = true
  }

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }
}


# DynamoDB Table for Terraform State Locking
resource "aws_dynamodb_table" "terraform_lock_table" {
  name           = "terraform-lock-table"
  hash_key       = "LockID"
  billing_mode   = "PAY_PER_REQUEST"
  attribute {
    name = "LockID"
    type = "S"
  }
}
