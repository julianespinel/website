FROM python:3-slim

# Install nginx
RUN apt-get update && apt-get install nginx vim -y --no-install-recommends
COPY ./docker/nginx.default /etc/nginx/sites-available/default

# Copy code and install dependencies
ENV PROJECT_ROOT /app
WORKDIR $PROJECT_ROOT
COPY . .
RUN pip install -r requirements.txt
CMD python manage.py collectstatic --settings=settings.base --noinput

EXPOSE 80
ENTRYPOINT ./docker/init-services.sh
