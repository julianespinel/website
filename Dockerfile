FROM python:3.8-slim

# Install nginx
RUN apt-get update && apt-get install gcc libc-dev nginx -y --no-install-recommends
COPY ./docker/nginx.default /etc/nginx/sites-available/default

# Copy code and install dependencies
ENV PROJECT_ROOT /app
WORKDIR $PROJECT_ROOT
COPY . .
RUN pip install -r requirements.txt
RUN python manage.py collectstatic --settings=settings.base --noinput

EXPOSE 80
ENTRYPOINT ./docker/init-services.sh
