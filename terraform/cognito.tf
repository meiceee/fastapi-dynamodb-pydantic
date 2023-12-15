# Cognito

resource "aws_cognito_user_pool" "techblog-nhat" {
  name = "techblog-nhat"
  username_attributes = [
    "email",
  ]
  auto_verified_attributes = [
    "email",
  ]
  schema {
    name                = "email"
    attribute_data_type = "String"
    mutable             = true
    required            = true
  }
  schema {
    name                = "name"
    attribute_data_type = "String"
    mutable             = true
    required            = true
  }
  password_policy {
    minimum_length    = 8
    require_lowercase = false
    require_numbers   = false
    require_symbols   = false
    require_uppercase = false
  }
  verification_message_template {
    default_email_option = "CONFIRM_WITH_CODE"
    email_message        = "Your verification code is {####}."
    email_subject        = "Your verification code"
  }
  email_configuration {
    email_sending_account = "COGNITO_DEFAULT"
  }
  tags = {
    Name = "techblog-nhat"
  }
}

resource "aws_cognito_user_pool_client" "techblog-nhat" {
  name         = "techblog-nhat"
  user_pool_id = aws_cognito_user_pool.techblog-nhat.id

  explicit_auth_flows = [
    "ALLOW_USER_PASSWORD_AUTH",
    "ALLOW_REFRESH_TOKEN_AUTH",
  ]
  generate_secret = false
}
