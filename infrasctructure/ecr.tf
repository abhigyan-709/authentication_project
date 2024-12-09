resource "aws_ecr_repository" "auth_repo" {
  name                 = "auth_app_repo"
  image_scanning_configuration {
    scan_on_push = true
  }
  image_tag_mutability = "MUTABLE"
}
