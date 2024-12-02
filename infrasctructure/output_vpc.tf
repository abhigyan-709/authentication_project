output "vpc_id" {
  value = aws_vpc.eks_vpc.id
}

output "subnet_ids" {
  value = [aws_subnet.eks_subnet_a.id, aws_subnet.eks_subnet_b.id]
}
