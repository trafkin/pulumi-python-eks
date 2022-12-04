import pulumi_aws as aws

def subnets_filter(subnet_ids: aws.ec2.AwaitableGetSubnetIdsResult):
    """this function gets just one public subnet per zone"""
    new_subnets_id = []
    azs_used = []

    for id in subnet_ids.ids:
        subnet_details = aws.ec2.get_subnet(
            id=id
        )
        if subnet_details.map_public_ip_on_launch:
            if len(azs_used) < 1:
                new_subnets_id.append(id)
                azs_used.append(subnet_details.availability_zone)
            else:
                if (subnet_details.availability_zone not in azs_used):
                    azs_used.append(subnet_details.availability_zone)
                    new_subnets_id.append(id)

    print(azs_used)
    print(new_subnets_id)

    return new_subnets_id