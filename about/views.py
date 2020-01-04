from django.shortcuts import render

# Create your views here.


def index(request):
    # return HttpResponse('Hello world')
    return render(request, 'about/index.html')
