python manage.py makemigrations --settings=settings.prod
python manage.py migrate --settings=settings.prod
python manage.py copy_version --settings=settings.prod
python manage.py md_to_html --settings=settings.prod
service nginx start
gunicorn website.wsgi
