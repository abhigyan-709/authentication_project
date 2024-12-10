# Provider Configuration
provider "aws" {
  region = "ap-south-1"
}

# ECR Repository
resource "aws_ecr_repository" "auth_repo" {
  name = "auth_app_repo"

  image_scanning_configuration {
    scan_on_push = true
  }

  image_tag_mutability = "MUTABLE"

  lifecycle {
    prevent_destroy = true
  }
}

# Output the Repository URL
output "repository_url" {
  value = aws_ecr_repository.auth_repo.repository_url
}

# Data Block for Existing IAM Policy
data "aws_iam_policy" "existing_policy" {
  name = "ECRAccessPolicy"
}

# IAM Policy for ECR Access
resource "aws_iam_policy" "ecr_policy" {
  count       = length(data.aws_iam_policy.existing_policy.id) == 0 ? 1 : 0
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

  lifecycle {
    prevent_destroy = true
  }
}

# IAM User
resource "aws_iam_user" "ecr_user" {
  name = "ecr_user"

  lifecycle {
    prevent_destroy = true
  }
}

# Attach the Policy to the IAM User
resource "aws_iam_user_policy_attachment" "ecr_policy_attachment" {
  user = aws_iam_user.ecr_user.name

  policy_arn = length(aws_iam_policy.ecr_policy) > 0 
    ? aws_iam_policy.ecr_policy[0].arn 
    : data.aws_iam_policy.existing_policy.arn

  lifecycle {
    prevent_destroy = true
  }
}

# IAM Role for Role Assumption
resource "aws_iam_role" "ecr_role" {
  name = "ECRRole"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = {
          Service = "ec2.amazonaws.com"
        },
        Action = "sts:AssumeRole"
      }
    ]
  })

  lifecycle {
    prevent_destroy = true
  }
}

# Attach the Policy to the Role
resource "aws_iam_role_policy_attachment" "ecr_role_policy_attachment" {
  role = aws_iam_role.ecr_role.name

  policy_arn = length(aws_iam_policy.ecr_policy) > 0 
    ? aws_iam_policy.ecr_policy[0].arn 
    : data.aws_iam_policy.existing_policy.arn

  lifecycle {
    prevent_destroy = true
  }
}
