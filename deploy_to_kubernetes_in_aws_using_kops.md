# Deploy to Kubernetes in AWS using Kops

This file describes how to deploy our website to a Kubernetes cluster in AWS using Kops.

## Setup cluster

### Define environment variables
```
export BUCKET_NAME=kops-k8s-website-bucket
export KOPS_STATE_STORE=s3://${BUCKET_NAME}
export ROUTE53_KOPS_DNS=cluster.jespinel.com
```

### Create cluster
```
kops create cluster \
  --name ${ROUTE53_KOPS_DNS} \
  --ssh-public-key=~/.ssh/id_rsa.pub \
  --cloud aws \
  --zones us-east-1a,us-east-1b,us-east-1c \
  --state ${KOPS_STATE_STORE} \
  --master-size t3.micro \
  --master-count 1 \
  --node-size t3.micro \
  --node-count 2 \
  --yes
```

## Deploy website

To deploy the website to our new k8s cluster we should do the following:

Check current kubectl context: `kubectl config current-context`, it should return: `cluster.jespinel.com`

1. `cd k8s/aws/`
1. `kubectl apply -f postgres/`
1. `kubectl apply -f django/`

### Fix load balancer health check in AWS

1. Go to: AWS console -> EC2 -> Load balancers
1. Select the kubernetes load balancer
1. Select the Health check tab
1. Modify it to:
```
Ping protocol: HTTP
Ping path: /blog/
```

### Install the k8s dashboard

1. Add dashboard to cluster: `kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.0.0/aio/deploy/recommended.yaml`
1. Create dashboard user: `kubectl apply -f dashboard/`
1. `kubectl proxy`
1. Get token for dashboard: `kubectl -n kubernetes-dashboard describe secret $(kubectl -n kubernetes-dashboard get secret | grep admin-user | awk '{print $1}')`
1. Copy token
1. Go to: http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/
1. Paste the token

### Check website on browser

1. Once in the k8s dashboard, on the bottom left click on `services`
1. In the `website-service` row you will see a link, click on it.

### How to deploy a new version

1. Modify the code
1. Create a new version of the Docker image, for example: `docker build -t website:1.0.2 .`
1. Update the new Docker image to AWS ECR
1. Update the Docker image version in the file `k8s/aws/django/deployment.yaml`
1. Send the changes to the cluster: `kubectl apply -f k8s/aws/django/deployment.yml`

## How to auto-scale k8s cluster

See: https://varlogdiego.com/kubernetes-cluster-with-autoscaling-on-aws-and-kops

## Tear down

### Delete cluster

```
kops delete cluster \
--state ${KOPS_STATE_STORE} \
--name ${ROUTE53_KOPS_DNS} \
--yes
```

## Resources

* https://medium.com/@markgituma/kubernetes-local-to-production-with-django-5-deploy-to-aws-using-kops-with-rds-postgres-6f913bcab622
* https://github.com/kubernetes/kops
* https://kubernetes.io/docs/tasks/access-application-cluster/web-ui-dashboard/
* https://github.com/kubernetes/dashboard/blob/master/docs/user/access-control/creating-sample-user.md
* https://dev.to/arswaw/create-a-subdomain-in-amazon-route53-in-2-minutes-3hf0
