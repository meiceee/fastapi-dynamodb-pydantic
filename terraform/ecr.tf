# Elastic Container Registry (ECR)
resource "aws_ecr_repository" "fastapi_ecr" {
  name = "fastapi-lunch-blog-app-ecr"
}