docker run -it -p 80:80 \
     -e POSTGRES_DB=<db-name> \
     -e POSTGRES_USER=<username> \
     -e POSTGRES_PASSWORD=<passowrd> \
     -e POSTGRES_HOST=<host> \
     -e POSTGRES_PORT=5432 \
     -e DJANGO_LOG_LEVEL=INFO \
     -e DJANGO_SETTINGS_MODULE=settings.local \
  website:1.0.6
