# Deploy to AWS using S3 and CloudFront

This deployment uses Pelican (a static site generator), AWS S3 and AWS
CloudFront.

## S3 and CloudFront

We are using the following services from AWS:

- S3: to store our static content, aka: html, css, images, etc.
- CloudFront: to serve our static content using a CDN.

### S3 configuration

To configure your S3 bucket keep the following in mind:

In the properties tab:

1. Keep the static web hosting option disabled

In the permissions tab:

1. Block all public access

### CloudFront configuration

To configure your CloudFront distribution keep the following in mind:

In the general tab:

1. Add your SSL certificate to serve content using HTTPS
1. Use the latest version of TLS
1. Set a default root object. In our case: `index.html`

In the origins tab:

1. Reference the S3 bucket you are using to store the content
1. Use an OAI to allow your CloudFront distribution to access the S3 bucket
   1. Select the option: `Yes, update the bucket policy`

It will add a policy similar to this one in your S3 bucket:

(If you plan to copy/paste please change the values in the placeholder `<>`)

```json
{
    "Version": "2008-10-17",
    "Id": "PolicyForCloudFrontPrivateContent",
    "Statement": [
        {
            "Sid": "1",
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::cloudfront:user/CloudFront Origin Access Identity <distribution-id>"
            },
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::<bucket-name>/*"
        }
    ]
}
```

In the behaviors tab:

1. Set your S3 bucket as the origin
1. Compress objects automatically
1. Redirect HTTP to HTTPS

### AIM configuration

We wanted to be able to deploy from our localhost by issuing a single command.
Deploying in this case means:

1. Upload new or modified files to S3
1. Invalidate our CloudFront distribution cache (optional, only if we don't want
   to wait for the cache to be automatically invalidated)

To do that we needed to create a user that could consume the AWS API to automate
this process. We used IAM to create the user and assign the minimum required
permissions to be able to execute the tasks. Let's see how we can do that:

To create a policy please go to IAM -> Access management -> Policies

Then, create a new policy with the following specification:

(Replace the values in the placeholder `<>`)

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "s3:ListBucket",
                "cloudfront:ListInvalidations",
                "cloudfront:GetInvalidation",
                "cloudfront:CreateInvalidation"
            ],
            "Resource": [
                "arn:aws:s3:::<bucket-name>/*",
                "arn:aws:s3:::<bucket-name>",
                "arn:aws:cloudfront::<account-id>:distribution/<distribution-id>"
            ]
        }
    ]
}
```

To create an API user please go to IAM -> Access management -> Users

Then, create a new API user by selecting the option `Access key - Programmatic access`.

Finally associate the new policy to the new user.

# Deployment

Finally we created a Python script to deploy. The deployment process is a simple
as executing the following command in the terminal:

```bash
python deploy.py -uv minor
```

The `-uv` argument stands for update-version and can take the following
possible values:

- major
- minor
- patch

The full script can be found here: [deploy.py](../deploy.py)
