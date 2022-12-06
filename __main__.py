import iam
import subnets_filter
import pulumi
import pulumi_aws as aws
import variables

shared_vars = variables.Variables()
stack_name = shared_vars.stack_name

## Get an existing Vpc resource from AWS through it's ID
subnets_id = aws.ec2.get_subnet_ids(
    vpc_id=shared_vars.vpc_id
)

cluster_sg = aws.ec2.SecurityGroup(stack_name,
    description=stack_name,
    vpc_id=shared_vars.vpc_id,
    ingress=[aws.ec2.SecurityGroupIngressArgs(
        from_port=0,
        to_port=0,
        protocol="-1",
        cidr_blocks=["0.0.0.0/0"],
        ipv6_cidr_blocks=["::/0"]
    )],
    egress=[aws.ec2.SecurityGroupEgressArgs(
        from_port=0,
        to_port=0,
        protocol="-1",
        cidr_blocks=["0.0.0.0/0"],
        ipv6_cidr_blocks=["::/0"],
    )]
)

# Create an AWS cluster resource
eks_cluster = aws.eks.Cluster(
    stack_name,
    role_arn=iam.eks_role.arn,
    tags={
        'Name': stack_name,
    },
    vpc_config=aws.eks.ClusterVpcConfigArgs(
        public_access_cidrs=['0.0.0.0/0'],
        security_group_ids=[cluster_sg.id],
        subnet_ids=subnets_id.ids,
    ),
)

#Loadbalancer, configured to internal in this case
load_balancer = aws.lb.LoadBalancer(
    "load-balancer", 
    load_balancer_type="application", 
    security_groups=[cluster_sg.id],
    subnets= subnets_filter.subnets_filter(subnets_id),
    internal=True,
)
#Creating two nodes inside the cluster, without the args 'instance_types' it will default to 't3.medium'
#Several of these can be created according to the requirements of the application
node_group = aws.eks.NodeGroup(
    'eks-node-group',
    cluster_name=eks_cluster.name,
    node_role_arn=iam.ec2_role.arn,
    subnet_ids=subnets_filter.subnets_filter(subnets_id),
    tags={
        'Name': stack_name,
    },
    scaling_config=aws.eks.NodeGroupScalingConfigArgs(
        desired_size=2,
        max_size=2,
        min_size=1,
    ),
)

# Export the cluster's kubeconfig.
pulumi.export('cluster-name', eks_cluster.name)

