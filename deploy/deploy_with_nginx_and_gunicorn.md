# Deploy with Nginx and Gunicorn

## Nginx

We use Nginx for two main reasons:

1. To serve static files
1. To be a reverse proxy to our Gunicorn server

In order to do this please follow these steps:

1. Add to Nginx configuration file located here: `/etc/nginx/sites-enabled/default`
```
location /static {
        root /<absolute-path>/website/allstatic;
}

location / {
        proxy_pass http://127.0.0.1:8000;
}
```
1. `sudo service nginx restart`

## Gunicorn

It is used as an application server.

1. Copy static files into STATIC_ROOT: `python3 manage.py collectstatic`
1. Serve the Django project using Gunicorn: `gunicorn website.wsgi`
1. Go to: http://localhost/blog/

## Resources

Why to use Nginx and Gunicorn?
* https://vsupalov.com/what-is-gunicorn/
* https://serverfault.com/questions/331256/why-do-i-need-nginx-and-something-like-gunicorn
