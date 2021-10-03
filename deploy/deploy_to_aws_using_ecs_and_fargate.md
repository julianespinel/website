# Deploy to AWS using ECS and Fargate

## ECS and Fargate

In order to deploy to ECS please do the following:

1. Create a Docker image and upload it to ECR
1. Create a Task definition using the Docker image in ECR
1. Create a cluster using `Fargate` as default capacity provider strategy
1. Create a service inside the cluster to deploy the containers:
    1. Use `Fargate` as capacity provider for the service
    1. Select the cluster's public VPC and its subnets
    1. Set "Auto-assign public IP" as `DISABLED` to don't assign a public IP to each task
    1. Set or create a load balancer for your service
    1. Define how to auto-scale the service

Because the containers deployed by this service will not have access to public internet, we are going to use AWS
PrivateLink to allow them to connect to other AWS services using the private network. In this way the traffic between
our containers and other AWS services does not leave Amazon's private network.

## Internet connectivity

We have two options to provide internet to our instances deployed in the public VPC.

### Public VPC

The first option is to deploy our service tasks in a public VPC and enable the option
to auto-assign a public IP to each task.

See point 5.d in this link: [Running a Task Using the Fargate Launch Type](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs_run_task_fargate.html)

### PrivateLink

If we want to use a private VPC or we don't want to auto-assign an IP to our task intances,
then we can use AWS PrivateLink to allow our tasks to communicate with other AWS services required
to deploy the task.

**Important:**

When creating a PrivateLink endpoint make sure to assign it a security group that includes all the instances that
require to interact with it. For more information take a look here:
[Setting up AWS PrivateLink for Amazon ECS, and Amazon ECR](https://aws.amazon.com/blogs/compute/setting-up-aws-privatelink-for-amazon-ecs-and-amazon-ecr/)

To create the PrivateLink endpoints please follow these steps:

1. Go to the VPC service and click on "Endpoints" in the menu on the left of the page.
1. Create the following 4 endpoints:
    1. com.amazonaws.us-east-1.ecr.api
    1. com.amazonaws.us-east-1.ecr.dkr  
    1. com.amazonaws.us-east-1.s3
    1. com.amazonaws.us-east-1.logs

After this you should be able to run the website as a container in AWS ECS using Fargate.
Just go to the load balancers section in EC2, copy the DNS name of the load balancer and paste it in a browser.

## Domain name and HTTPS

### Domain name

To link the domain name with the load balancer please follow the steps in this link:
[Routing traffic to an ELB load balancer](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/routing-to-elb-load-balancer.html)

### Enforce HTTPS

To enforce https in the website, please follow the steps in this link:
[How can I redirect HTTP requests to HTTPS using an Application Load Balancer?](https://aws.amazon.com/premiumsupport/knowledge-center/elb-redirect-http-to-https-using-alb/)

## CI/CD using AWS CodeBuild and CodeDeploy

To implement a CI/CD pipeline using AWS CodePipeline, please follow the steps
described in this guide: [Tutorial: Continuous Deployment with CodePipeline](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-cd-pipeline.html)

If you get the following error:
```
Error while executing command: $(aws ecr get-login --region $AWS_DEFAULT_REGION --no-include-email). Reason: exit status 255
```
This is the solution: https://stackoverflow.com/a/55585104/2420718

Here you can find the [buildspec file reference](https://docs.aws.amazon.com/codebuild/latest/userguide/build-spec-ref.html) for AWS CodeBuild.

## Release

To release changes please follow these steps:

1. Create a new branch from master (what is in master is currently in prod)
1. Perform the required changes
1. Commit the changes to git
1. Increase the `IMAGE_VERSION` in the file `buildspec.yml` (Please follow Semver)
1. Commit the change in `buildspec.yml` to git
1. Push the branch and create a pull request to master
1. Merge the code if it meets the following conditions:
   1. All tests passes
   1. Static code analysis passes
1. AWS CodePipeline will automatically:
   1. Create the new Docker image and upload it to ECR.
   1. Deploy the new Docker image in the Fargate cluster.

## Resources

* https://aws.amazon.com/blogs/compute/setting-up-aws-privatelink-for-amazon-ecs-and-amazon-ecr/
* https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/routing-to-elb-load-balancer.html
* https://aws.amazon.com/premiumsupport/knowledge-center/elb-redirect-http-to-https-using-alb/
