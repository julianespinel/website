from django.db import connection
from django.http import HttpResponse


def index(request):
    with connection.cursor() as cursor:
        cursor.execute("select 1")
        one = cursor.fetchone()[0]
        if one != 1:
            raise Exception('Could not access the database')
    return HttpResponse("I'm healthy")
