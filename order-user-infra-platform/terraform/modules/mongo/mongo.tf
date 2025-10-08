resource "aws_security_group" "mongo" {
  name = "mongo-sg"
  vpc_id = var.vpc_id

  ingress {
    from_port = 27017
    to_port = 27017
    protocol = "tcp"
    security_groups = [var.eks_sg_id]
  }

  egress {
    from_port = 0
    to_port = 0
    protocol = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "mongo" {
  ami = var.ami_id
  instance_type = "t3.micro"
  subnet_id = var.subnet_id
  vpc_security_group_ids = [aws_security_group.mongo.id]
  associate_public_ip_address = false
}

data "aws_secretsmanager_secret_version" "creds" {
  secret_id = var.secret_arn
}