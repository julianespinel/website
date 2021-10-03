# website

This repository contains the code of the website: [jespinel.com](https://jespinel.com/)

This project was initiated with the following goals in mind:

1. Create a new version of the website where I could write blog posts in Markdown.
1. Learn how to deploy an application using Kubernetes in AWS.

**Update #1**

After achieving the first and second goals I realized that deploying using
Kubernetes in AWS was expensive. I ended using AWS ECS + Fargate + Code Pipeline
to deploy to prod. This solution provides the following benefits:

1. It is cheaper than deploying a k8s cluster in AWS.
1. I don't have to worry about the k8s cluster because AWS handles the Fargate cluster for me.
1. It allows me to automate the build and deployment processes. (CI/CD)

However, in the section [Deploy](#deploy)
of this file, you can find links to the documentation I generated when deployed
this system using Kubernetes. I have also documented my current deployment
process.

**Update #2**

I was spending around 30 USD/month to have this website running using the
following AWS services:

- Elastic Load Balancer
- ECR + ECS (Fargate)
- CodePipeline

Those services allowed the website to scale and deploy automatically. I was
happy with how the process worked. However, I knew I could do better. I wanted
to make changes with two goals in mind:

1. Reduce AWS costs
2. Generate the website content statically

That's why I made the following decisions:

1. Move from Django (dynamic content) to Pelican (static content).
2. Replace the AWS services I was using, by S3 and CloudFront only.

The current deployment is documented [here](deploy/deploy_to_aws_using_s3_and_cloudfront.md)

## Installation

Pre-requisites:

1. Install Python 3
1. Install pip
1. Install virtualenv: `pip install virtualenv`

Execute the following commands in the root directory of the project.

1. Create the virtual environment: `virtualenv venv`
1. Activate virtualenv: `source venv/bin/activate`
2. Install dependencies: `pip install -r requirements.txt`

## How to run?

### Development

To start the server and reloading the changes automatically use:

```bash
make devserver
```

Then go to: http://127.0.0.1:8000/

Create or modify files in the `content` directory.
Refresh the browser tab to see the changes.

For more information on Pelican please check their
[documentation](https://docs.getpelican.com/en/latest/)

**How to generate the pygments.css file?**
```bash
cd theme/static/css/
pygmentize -S monokai -f html > pygments.css
```

### Deploy

#### Current strategy

The current deployment strategy is automated by the Python script
[deploy.py](deploy.py).

You need two files to run the deployment script:

1. public.toml
1. secrets.toml

The `public.toml` file has the following structure:

```toml
[website]
url = ""
version = "x.y.z" # where x, y and z are positive integers
```

The `secrets.toml` file has the following structure:

```toml
[website]
google_analytics = ""

[aws]
access_key = ""
secret_key = ""
s3_bucket = ""
cloudfront_distribution_id = ""
```

After you create the files and add the required values, you can run the script
by typing in the terminal:

```bash
python deploy.py -uv minor
```

The `-uv` argument stands for update-version and can take the following
possible values:

- major
- minor
- patch

The AWS services and their configuration we are using is documented here:
[Deploy to AWS using S3 and CloudFront](deploy/deploy_to_aws_using_s3_and_cloudfront.md)

#### Previous strategies

I have tested various deployment strategies in this project. Here you can find
the documentation of them:

1. [Deploy with Nginx and Gunicorn](deploy/deploy_with_nginx_and_gunicorn.md)
1. [Deploy locally with Kubernetes (Minikube)](deploy/deploy_locally_with_kubernetes.md)
1. [Deploy to a Kubernetes cluster in AWS with Kops](deploy/deploy_to_kubernetes_in_aws_using_kops.md)
1. [Deploy to AWS using ECS and Fargate](deploy/deploy_to_aws_using_ecs_and_fargate.md)
1. [Deploy to AWS using S3 and CloudFront](deploy/deploy_to_aws_using_s3_and_cloudfront.md) <-- Currently in use
