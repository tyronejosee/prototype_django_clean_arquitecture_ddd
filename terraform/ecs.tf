resource "aws_ecs_cluster" "cluster" {
  name = var.project_name
}

resource "aws_cloudwatch_log_group" "ecs" {
  name              = "/ecs/${var.project_name}"
  retention_in_days = 7 # 14 min recommended
}

resource "aws_lb" "alb" {
  name               = "${var.project_name}-alb"
  internal           = false
  load_balancer_type = "application"
  subnets            = aws_subnet.public[*].id
  security_groups    = [aws_security_group.alb_sg.id]
}

resource "aws_lb_target_group" "tg" {
  name     = "${var.project_name}-tg"
  port     = var.container_port
  protocol = "HTTP"
  vpc_id   = aws_vpc.this.id
  health_check {
    path                = "/health-check"
    interval            = 30
    healthy_threshold   = 2
    unhealthy_threshold = 3
  }
}

resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.alb.arn
  port              = 80
  protocol          = "HTTP"
  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.tg.arn
  }
}

resource "aws_ecs_task_definition" "task" {
  family                   = "${var.project_name}-task"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "512"
  memory                   = "1024"
  execution_role_arn       = aws_iam_role.ecs_task_execution.arn
  task_role_arn            = aws_iam_role.ecs_task_role.arn
  container_definitions = jsonencode([{
    name         = "django"
    image        = var.image
    essential    = true
    portMappings = [{ containerPort = var.container_port, protocol = "tcp" }]

    logConfiguration = {
      logDriver = "awslogs"
      options = {
        awslogs-group         = aws_cloudwatch_log_group.ecs.name
        awslogs-region        = var.aws_region
        awslogs-stream-prefix = "django"
      }
    }
    environment = [
      # Project
      { name = "PROJECT_NAME", value = "Project Marketly" },
      { name = "PROJECT_DESCRIPTION", value = "This repository implements a Django application following the principles of Clean Architecture and Domain-Driven Design (DDD). It serves as a practical example of how to structure a robust and maintainable application." },
      { name = "PROJECT_VERSION", value = "0.1.0" },
      # Variables no secret
      { name = "DJANGO_PORT", value = tostring(var.container_port) },
      { name = "IS_RUNNING_PIPELINE", value = "False" },
      { name = "DEBUG", value = "False" },
      { name = "ALLOWED_HOSTS", value = "${aws_lb.alb.dns_name}" },
      # Storage
      { name = "AWS_S3_REGION_NAME", value = var.aws_region },
      { name = "AWS_S3_CUSTOM_DOMAIN", value = "${aws_s3_bucket.app_bucket.bucket}.s3.amazonaws.com" },
      # Documentation
      { name = "LICENCE_NAME", value = "MIT License" },
      { name = "LICENCE_URL", value = "https://github.com/tyronejose/project_marketly/blob/main/LICENSE" },
      { name = "CONTACT_NAME", value = "Tyrone Jose" },
      { name = "CONTACT_URL", value = "https://github.com/tyronejose" },
      # Database & Cache
      { name = "POSTGRES_DB", value = var.db_name },
      { name = "POSTGRES_USER", value = var.db_username },
      { name = "POSTGRES_HOST", value = aws_db_instance.postgres.address },
      { name = "POSTGRES_PORT", value = "5432" },
      { name = "REDIS_PORT", value = "6379" },
      { name = "CACHE_LOCATION", value = "redis://${aws_elasticache_cluster.redis.cache_nodes[0].address}:6379/0" },
    ]
    secrets = [
      # Project
      { name = "POSTGRES_PASSWORD", valueFrom = aws_secretsmanager_secret_version.db_password_version.arn },
      { name = "DJANGO_SECRET_KEY", valueFrom = aws_secretsmanager_secret_version.django_secret_version.arn },
      # AWS
      { name = "AWS_ACCESS_KEY_ID", valueFrom = aws_secretsmanager_secret_version.aws_access_key_version.arn },
      { name = "AWS_SECRET_ACCESS_KEY", valueFrom = aws_secretsmanager_secret_version.aws_secret_key_version.arn },
      # Payment
      { name = "PAYPAL_CLIENT_ID", valueFrom = aws_secretsmanager_secret_version.paypal_client_id_version.arn },
      { name = "PAYPAL_CLIENT_SECRET", valueFrom = aws_secretsmanager_secret_version.paypal_client_secret_version.arn }
    ]
  }])
}

resource "aws_ecs_service" "service" {
  name            = "${var.project_name}-svc"
  cluster         = aws_ecs_cluster.cluster.id
  task_definition = aws_ecs_task_definition.task.arn
  desired_count   = 1
  launch_type     = "FARGATE"
  network_configuration {
    subnets          = aws_subnet.private[*].id
    security_groups  = [aws_security_group.ecs_sg.id]
    assign_public_ip = false
  }
  load_balancer {
    target_group_arn = aws_lb_target_group.tg.arn
    container_name   = "django"
    container_port   = var.container_port
  }

  depends_on = [aws_lb_listener.http]
}
