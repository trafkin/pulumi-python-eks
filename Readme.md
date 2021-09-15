# AWS Kubernetes Cluster

These scripts deploy an EKS Kubernetes cluster inside an existing VPC resource from AWS

## Prerequisites

1. [Install Pulumi](https://www.pulumi.com/docs/get-started/install/)
1. [Configure Pulumi for AWS](https://www.pulumi.com/docs/intro/cloud-providers/aws/setup/)
1. [Configure Pulumi for Python](https://www.pulumi.com/docs/intro/languages/python/)

## How to run and deploy

1.  Create a new stack with any name you need:

    ```
    $ pulumi stack init eks-project
    ```

2.  Set the AWS region (example below):

    ```
    $ pulumi config set aws:region us-east-2
    ```

3.  Run `pulumi preview` to preview, and deploy changes by `pulumi up` 
4.  View the cluster name via `stack output`
5.  Verify that the EKS cluster exists, by either using the AWS Console or running `aws eks list-clusters`.

6. Update your KubeConfig, Authenticate to your Kubernetes Cluster and verify you have API access and nodes running, in case of missing the permissions to access nodes please visit this [page](https://docs.aws.amazon.com/eks/latest/userguide/add-user-role.html)
