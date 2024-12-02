resource "aws_ecr_repository" "my_repo" {
  name                 = "my-python-app-repo"
  image_scanning_configuration {
    scan_on_push = true
  }
  image_tag_mutability = "MUTABLE"
}
