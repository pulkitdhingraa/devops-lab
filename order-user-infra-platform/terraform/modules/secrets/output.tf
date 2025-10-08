output "pg_secret_arn" {
  value = aws_secretsmanager_secret_version.postgres.arn
}

output "mongo_secret_arn" {
  value = aws_secretsmanager_secret_version.mongo.arn
}