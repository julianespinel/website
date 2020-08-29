# website

This repository contains the code of my personal website: [jespinel.com](https://jespinel.com/)

This project initiated with the following goals in mind:

1. Create a new version of my website where I could write blog posts in Markdown.
1. Learn how to deploy an application using Kubernetes in AWS.

After achieving the first and second goals I realised that deploying using Kubernetes in AWS was expensive.
I ended using AWS ECS + Fargate + Code Pipeline to deploy to prod. This solution provides the following benefits:

1. It is cheaper than deploying a k8s cluster in AWS.
1. I don't have to worry about the k8s cluster because AWS handles the Fargate cluster for me.
1. It allows me to automate the build and deployment processes. (CI/CD)

However, in the section [Deploy](https://github.com/julianespinel/website#deploy) of this file, you can find links
to the documentation I generated when deployed this system using Kubernetes.<br>
I have also documented my current deployment process.

## Installation

Pre-requisites:

1. Install Python 3
1. Install pip 3
1. Install virtualenv: `pip3 install virtualenv`

Execute the following commands in the root directory of the project.

1. Create the virtual environment: `virtualenv venv`
1. Activate virtualenv: `source venv/bin/activate`
1. Install django: `python3 -m pip install Django`
1. Install dependencies: `pip install -r requirements.txt`

## Tests

Please execute the following steps to run the tests:

1. Start a Docker container with Postgres on port 5432: `docker-compose up -d`
1. Run: `python manage.py test --settings=settings.test`

## How to run?

### Development

1. Start Docker compose: `docker-compose up -d`
1. Add user to database
   1. `psql -h localhost -p 5432 -U postgres`
   1. `CREATE DATABASE websitedb;`
   1. `CREATE USER websiteuser WITH ENCRYPTED PASSWORD 'password';`
   1. `GRANT ALL PRIVILEGES ON DATABASE websitedb TO websiteuser;`
   1. `\q`
1. Run migrations: `python manage.py makemigrations --settings=settings.local`
1. Run migrations: `python manage.py migrate --settings=settings.local`
1. Convert posts in Markdown to HTML: `python manage.py md_to_html --settings=settings.local`
1. Start server: `python manage.py runserver --settings=settings.local`

**How to generate the pygments.css file?**
```bash
pygmentize -S default -f html > pygments.css
```

### Deploy

I tested various deployment strategies in this project. Here you can find the documentation of them:

1. [Deploy with Nginx and Gunicorn](./deploy_with_nginx_and_gunicorn.md)
1. [Deploy locally with Kubernetes (Minikube)](./deploy_locally_with_kubernetes.md)
1. [Deploy to a Kubernetes cluster in AWS with Kops](./deploy_to_kubernetes_in_aws_using_kops.md)
1. [Deploy to AWS using ECS and Fargate](./deploy_to_aws_using_ecs_and_fargate.md) <-- Currently in use

### CI/CD using AWS CodeBuild and CodeDeploy

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

## Supported URLs

* Index: `/`
* Blog: `/blog`
* Health check: `/health`

## How does the blog work?

See: [Blog README](./blog/README.md)
