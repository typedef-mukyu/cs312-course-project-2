terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}

provider "aws" {
  region = "us-west-2"
}

resource "aws_instance" "mcserver" {
  ami           = "ami-0eb9d67c52f5c80e5"
  instance_type = "t2.small"
#   network_interface {
#     network_interface_id = aws_network_interface.mcserver-netif0.id
#     device_index         = 0
#   }
  associate_public_ip_address = true
  vpc_security_group_ids      = [aws_security_group.mcserversg.id]
  tags = {
    Name = "MinecraftServer"
  }
}
resource "aws_key_pair" "deployer" {
  key_name   = "minecraft-server-key"
  public_key = var.ssh_public_key
}
# resource "aws_vpc" "mcvpc" {
#   cidr_block = "10.3.12.0/24"
#   tags = {
#     Name = "Minecraft VPC"
#   }
# }
# resource "aws_subnet" "mcvpcs0" {
#   vpc_id            = aws_vpc.mcvpc.id
#   cidr_block        = "10.3.12.0/28"
#   availability_zone = "us-west-2a"
#   tags = {
#     Name = "Minecraft Server VPC Subnet 0"
#   }
# }
# resource "aws_network_interface" "mcserver-netif0" {
#   subnet_id  = aws_subnet.mcvpcs0.id
#   private_ip = "10.3.12.2"
#   tags = {
#     Name = "Minecraft Server Network Interface"
#   }
# }
resource "aws_security_group" "mcserversg" {
  name        = "minecraft-secgrp"
  description = "Allow SSH and Minecraft game traffic (port 25565) to all ports"
  #vpc_id      = aws_vpc.mcvpc.id
  tags = {
    name = "minecraft-secgrp"
  }
}
resource "aws_vpc_security_group_ingress_rule" "allow_ssh" {
  security_group_id = aws_security_group.mcserversg.id
  cidr_ipv4         = "0.0.0.0/0"
  from_port         = 22
  ip_protocol       = "tcp"
  to_port           = 22
}
resource "aws_vpc_security_group_ingress_rule" "allow_mc_tcp" {
  security_group_id = aws_security_group.mcserversg.id
  cidr_ipv4         = "0.0.0.0/0"
  from_port         = 25565
  ip_protocol       = "tcp"
  to_port           = 25565
}
resource "aws_vpc_security_group_ingress_rule" "allow_mc_udp" {
  security_group_id = aws_security_group.mcserversg.id
  cidr_ipv4         = "0.0.0.0/0"
  from_port         = 25565
  ip_protocol       = "udp"
  to_port           = 25565
}
resource "aws_vpc_security_group_egress_rule" "allow_outbound" {
  security_group_id = aws_security_group.mcserversg.id
  cidr_ipv4         = "0.0.0.0/0"
  ip_protocol       = "-1"
}