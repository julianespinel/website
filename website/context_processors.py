from django.conf import settings

def google_analytics_key(request):
    return {'GOOGLE_ANALYTICS_KEY': settings.GOOGLE_ANALYTICS_KEY}

def docker_image_version(request):
    image = settings.DOCKER_IMAGE.split(":")
    version = "local" if len(image) < 2 else image[1]
    return {'DOCKER_IMAGE_VERSION': version}
