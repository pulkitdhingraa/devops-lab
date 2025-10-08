provider "aws" {
  region = "ap-south-2"
}

# vpc and subnet (with az)

resource "aws_vpc" "web_vpc" {
  cidr_block = var.vpc_cidr
}

data "aws_availability_zones" "available_zones" {}

resource "aws_subnet" "private_subnet" {
  vpc_id = aws_vpc.web_vpc.id
  cidr_block = var.private_cidr
  availability_zone = data.aws_availability_zones.available_zones.names[0]

  tags = {
    Name = "private-subnet"
  }
}

resource "aws_subnet" "public_subnet" {
  count = length(var.public_cidr)
  vpc_id = aws_vpc.web_vpc.id
  cidr_block = var.public_cidr[count.index]
  availability_zone = data.aws_availability_zones.available_zones.names[count.index]
  map_public_ip_on_launch = true

  tags = {
    Name = "public-subnet-${count.index + 1}"
  }
}

# internet gateway, nat gw, route table and its associations

resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.web_vpc.id

  tags = {
    Name = "igw"
  }
}

resource "aws_route_table" "public_rt" {
  vpc_id = aws_vpc.web_vpc.id
  route {
    cidr_block = "0.0.0.0/0"    # anything going to this cidr block from our aws will go to igw
    gateway_id = aws_internet_gateway.igw.id
  }
}

resource "aws_route_table_association" "public_rt_asso" {
  count = length(aws_subnet.public_subnet)
  subnet_id = aws_subnet.public_subnet[count.index].id  # traffic coming from resources in this particular subnet
  route_table_id = aws_route_table.public_rt.id
}

resource "aws_eip" "nat_ip" {
  domain = "vpc"
}

resource "aws_nat_gateway" "nat" {
  allocation_id = aws_eip.nat_ip.id
  subnet_id = aws_subnet.public_subnet[0].id

  tags = {
    Name = "nat-gw"
  }

  depends_on = [aws_internet_gateway.igw]
}

resource "aws_route_table" "private_rt" {
  vpc_id = aws_vpc.web_vpc.id
  route {
    cidr_block = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.nat.id
  }
}

resource "aws_route_table_association" "private_rt_asso" {
  subnet_id = aws_subnet.private_subnet.id
  route_table_id = aws_route_table.private_rt.id
}

# security groups - 1 for alb 1 for ec2 instances

resource "aws_security_group" "alb_sg" {
  name = "alb-sg"
  vpc_id = aws_vpc.web_vpc.id

  ingress {
    description = "Allow HTTP"
    from_port = 80
    to_port = 80
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port = 0
    to_port = 0
    protocol = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  tags = {
    Name = "alb-sg"
  }
}

resource "aws_security_group" "ec2-sg" {
  name = "ec2-sg"
  vpc_id = aws_vpc.web_vpc.id

  ingress {
    from_port = 80
    to_port = 80
    protocol = "tcp"
    security_groups = [aws_security_group.alb_sg.id]
  }

  ingress {
    from_port = 22
    to_port = 22
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port = 0
    to_port = 0
    protocol = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "ec2-sg"
  }
}

# ec2-instance with userdata

# resource "aws_instance" "web" {
#   ami = var.ami
#   instance_type = "t3.micro"
#   vpc_security_group_ids = [aws_security_group.ec2-sg.id]
#   subnet_id = aws_subnet.private_subnet.id
#   associate_public_ip_address = false
#   key_name = "web"

#   user_data_base64 = filebase64(var.userdatafile)
#   user_data_replace_on_change = true
# }

# ec2-instance with provisioner

resource "aws_instance" "web" {
  ami = var.ami
  instance_type = "t3.micro"
  vpc_security_group_ids = [aws_security_group.ec2-sg.id]
  subnet_id = aws_subnet.private_subnet.id
  associate_public_ip_address = false
  key_name = "web"

  provisioner "file" {
    source = "index.html"
    destination = "/tmp/index.html"

    connection {
      type = "ssh"
      user = "ec2-user"
      private_key = file("web.pem")
      host = self.public_ip
    }
  }

  provisioner "remote-exec" {
    inline = [ 
        "sudo yum update -y",
        "sudo amazon-linux-extras install -y nginx1",
        "sudo systemctl start nginx",
        "sudo systemctl enable nginx",
        "sudo mv /tmp/index.html /usr/share/nginx/html/index.html",
        "sudo chown nginx:nginx /usr/share/nginx/html/index.html" 
     ]

    connection {
      type = "ssh"
      user = "ec2-user"
      private_key = file("web.pem")
      host = self.public_ip
    }
  }
}

# application load balancer, target group and attachments, listener

resource "aws_alb" "alb" {
  name = "alb"
  internal = false
  load_balancer_type = "application"

  security_groups = [aws_security_group.alb_sg.id]
  subnets = [for subnet in aws_subnet.public_subnet : subnet.id]

  tags = {
    Name = "web"
  }
}

resource "aws_alb_target_group" "tg" {
  name = "alb-tg"
  port = 80
  protocol = "HTTP"
  vpc_id = aws_vpc.web_vpc.id

  health_check {
    path = "/"
    protocol = "HTTP"
    port = "80"
  }
}

resource "aws_alb_target_group_attachment" "tg-att" {
  target_group_arn = aws_alb_target_group.tg.arn
  target_id = aws_instance.web.id
  port = 80
}

resource "aws_alb_listener" "alb-listener" {
  load_balancer_arn = aws_alb.alb.arn
  port = 80
  protocol = "HTTP"

  default_action {
    target_group_arn = aws_alb_target_group.tg.arn
    type = "forward"
  }
}

output "loadbalancerdns" {
  value = aws_alb.alb.dns_name
}