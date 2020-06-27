python manage.py md_to_html --settings=settings.prod
service nginx start
gunicorn website.wsgi