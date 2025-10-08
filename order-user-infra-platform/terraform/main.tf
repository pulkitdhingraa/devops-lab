module "vpc" {
  source = "./modules/vpc"
  vpc_name = var.vpc_name
  cidr_block = var.cidr_block
  private_subnets = var.private_subnets
  public_subnets = var.public_subnets
}

module "eks" {
  source = "./modules/eks"
  cluster_name = var.cluster_name
  vpc_id = module.vpc.vpc_id
  private_subnet_ids = module.vpc.private_subnet_ids
}

# module "secrets" {
#   source = "./modules/secrets"
#   mongo_secret = var.mongo_secret
#   postgres_secret = var.postgres_secret
# }

# module "s3" {
#   source = "./modules/s3"
# }

# module "rds" {
#   source = "./modules/rds"
#   vpc_id = module.vpc.vpc_id
#   subnet_ids = module.vpc.private_subnet_ids
#   secret_arn = module.secrets.pg_secret_arn
#   eks_sg_id = module.eks.eks_sg_id
# }

# module "mongo" {
#   source = "./modules/mongo"
#   vpc_id = module.vpc.vpc_id
#   subnet_id = module.vpc.private_subnet_ids[0]
#   secret_arn = module.secrets.mongo_secret_arn
#   ami_id = var.mongo_ec2_ami_id
#   eks_sg_id = module.eks.eks_sg_id
# }