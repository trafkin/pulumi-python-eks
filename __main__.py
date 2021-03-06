"""An AWS Python Pulumi program"""
import iam
import pulumi
import pulumi_aws as aws


## Get an existing Vpc resource from AWS through it's ID
vpc = aws.ec2.get_vpc(id="")

# Create an AWS cluster resource
eks_cluster = aws.eks.Cluster(
    'eks-cluster',
    role_arn=iam.eks_role.arn,
    tags={
        'Name': 'pulumi-eks-cluster',
    },
    vpc_config=aws.eks.ClusterVpcConfigArgs(
        public_access_cidrs=['0.0.0.0/0'],
        security_group_ids=[vpc.eks_security_group.id],
        subnet_ids=[vpc.vpc_subnet.id, vpc.vpc_subnet_two.id],
    ),
)

#Loadbalancer, configured to internal in this case
load_balancer = aws.lb.LoadBalancer(
    "load-balancer", 
    load_balancer_type="application", 
    security_groups=[vpc.eks_security_group.id],
    subnets=[vpc.vpc_subnet.id, vpc.vpc_subnet_two.id],
    internal=True,
)
#Creating two nodes inside the cluster, without the args 'instance_types' it will default to 't3.medium'
#Several of these can be created according to the requirements of the application
node_group = aws.eks.NodeGroup(
    'eks-node-group',
    cluster_name=eks_cluster.name,
    node_role_arn=iam.ec2_role.arn,
    subnet_ids=[vpc.vpc_subnet.id],
    tags={
        'Name': 'pulumi-cluster-nodeGroup',
    },
    scaling_config=aws.eks.NodeGroupScalingConfigArgs(
        desired_size=2,
        max_size=2,
        min_size=1,
    ),
)

# Export the cluster's kubeconfig.
pulumi.export('cluster-name', eks_cluster.name)

