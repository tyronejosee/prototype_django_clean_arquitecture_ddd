resource "aws_secretsmanager_secret" "db_password" {
  name = "${var.project_name}-db-password"
}

resource "aws_secretsmanager_secret_version" "db_password_version" {
  secret_id     = aws_secretsmanager_secret.db_password.id
  secret_string = var.db_password
}

resource "aws_secretsmanager_secret" "django_secret" {
  name = "${var.project_name}-django-secret"
}

resource "aws_secretsmanager_secret_version" "django_secret_version" {
  secret_id     = aws_secretsmanager_secret.django_secret.id
  secret_string = var.django_secret_key
}

resource "aws_secretsmanager_secret" "aws_access_key" {
  name = "${var.project_name}-aws-access-key"
}

resource "aws_secretsmanager_secret_version" "aws_access_key_version" {
  secret_id     = aws_secretsmanager_secret.aws_access_key.id
  secret_string = var.aws_access_key_id
}

resource "aws_secretsmanager_secret" "aws_secret_key" {
  name = "${var.project_name}-aws-secret-key"
}

resource "aws_secretsmanager_secret_version" "aws_secret_key_version" {
  secret_id     = aws_secretsmanager_secret.aws_secret_key.id
  secret_string = var.aws_secret_access_key
}

resource "aws_secretsmanager_secret" "paypal_client_id" {
  name = "${var.project_name}-paypal-client-id"
}

resource "aws_secretsmanager_secret_version" "paypal_client_id_version" {
  secret_id     = aws_secretsmanager_secret.paypal_client_id.id
  secret_string = var.paypal_client_id
}

resource "aws_secretsmanager_secret" "paypal_client_secret" {
  name = "${var.project_name}-paypal-client-secret"
}

resource "aws_secretsmanager_secret_version" "paypal_client_secret_version" {
  secret_id     = aws_secretsmanager_secret.paypal_client_secret.id
  secret_string = var.paypal_client_secret
}
