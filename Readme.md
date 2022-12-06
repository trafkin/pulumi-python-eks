# AWS Kubernetes Cluster

These scripts deploy an EKS Kubernetes cluster inside an existing VPC resource from AWS

## Prerequisites

- [Install Pulumi](https://www.pulumi.com/docs/get-started/install/)
- [Configure Pulumi for AWS](https://www.pulumi.com/docs/intro/cloud-providers/aws/setup/)
- [Configure Pulumi for Python](https://www.pulumi.com/docs/intro/languages/python/)
- [sops](https://github.com/mozilla/sops)
## How to run and deploy a new EKS cluster

1. Create a `variables.py` file, like the following example:

    ```
    class Variables:
        vpc_id     = "vpc-xxxxxxxxx"
        """VPC ID where the EKS cluster is going to be deployed"""
        
        stack_name = "prod_cluster"
        """Name for the resources linked to this EKS"""
    ```

2. Create a new stack with any name you need:

    ```
    $ pulumi stack init eks-project
    ```

3.  Set the AWS region (example below):

    ```
    $ pulumi config set aws:region us-east-2
    ```

4.  Run `pulumi preview` to preview, and deploy changes by `pulumi up` 
5.  View the cluster name via `stack output`
6.  Verify that the EKS cluster exists, by either using the AWS Console or running `aws eks list-clusters`.

7. Update your KubeConfig, Authenticate to your Kubernetes Cluster and verify you have API access and nodes running, in case of missing the permissions to access nodes please visit this [page](https://docs.aws.amazon.com/eks/latest/userguide/add-user-role.html)

## How to encrypt/decrypt stack files

Linux:

Define the `KMS key` that you are going to use and be sure that your `AWS CLI` is pointing to the correct AWS account
```
export SOPS_KMS_ARN=arn:aws:kms:REGION:ACCOUNT-ID:alias/ALIAS-NAME
```

- Encrypt:
```
sops -e NAME-OF-YOUR-STACK.json > stacks/NAME-OF-YOUR-STACK.enc
```

- Decrypt:
```
sops --output-type json -d NAME-OF-YOUR-STACK.enc > NAME-OF-YOUR-STACK.json
```

## How to use/update a running cluster
If you need to update/change anything on a living cluster created by this same stack, follow the below steps:

1. Decrypt the stack file that you are going to use. (see "How to encrypt/decrypt stack files" section)
2. Clone the repository
3. you should import the stack that you want to use/update, create a stack for this new import (also, you can use default stack)

    ```
    $ pulumi stack import --file stack.json
    ```
4. Run `pulumi preview` to preview, and deploy changes by `pulumi up`  (using the stack created in the before step), also you need to create the `variables.py` file **with the correct variables, if any variable is different it's going to update the current stack wth unwanted changes**, right after importing the stack and defining the `variables.py` run a `pulumi preview` the output should indicate no changes. (maybe some `messages` outputs)

## How to keep changes as code
if you update a living cluster shared with a team then it's necessary to update/create a stack file.
if you are updating a stack the name of the file should be the same as you received, if not, you can choose the name. 
```
pulumi stack export --file stack.json
```
Encrypt the file (see "How to encrypt/decrypt stack files" section) and save it in `stacks` folder then push the changes.