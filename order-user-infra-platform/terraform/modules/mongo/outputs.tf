output "mongo_ec2_id" {
    value = aws_instance.mongo.id
}

output "mongo_ec2_host_id" {
  value = aws_instance.mongo.host_id
}