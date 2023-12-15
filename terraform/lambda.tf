# IAM Role for Lambda
resource "aws_iam_role" "lambda" {
  name = "FastAPILunchBlogLambdaRole"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "lambda.amazonaws.com",
        },
      },
    ],
  })
}

resource "aws_iam_role_policy_attachment" "lambda" {
  role       = aws_iam_role.lambda.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy_attachment" "dynamodb" {
  role       = aws_iam_role.lambda.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess"
}

# Lambda Function
resource "aws_lambda_function" "fastapi_lunch_blog_lambda" {
  function_name = "FastAPILunchBlogLambdaFunction"
  role          = aws_iam_role.lambda.arn
  package_type  = "Image"
  image_uri     = "${aws_ecr_repository.fastapi_ecr.repository_url}:latest"

  environment {
    variables = {
      LOG_LEVEL                       = "INFO"
      POWERTOOLS_METRICS_NAMESPACE    = "FastAPILunchBlog"
      POWERTOOLS_SERVICE_NAME         = "FastAPILunchBlog"
      DYNAMODB_LUNCH_BLOG_TABLE = aws_dynamodb_table.lunch_blog.name
    }
  }
}
