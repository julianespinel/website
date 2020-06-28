from django.conf import settings


def google_analytics_key(request):
    return {'GOOGLE_ANALYTICS_KEY': settings.GOOGLE_ANALYTICS_KEY}


def docker_image_version(request):
    version = "local"
    try:
        image = settings.DOCKER_IMAGE_VERSION
        if image:
            array = image.split(":")
            version = array[1] if len(array) > 1 else image
    finally:
        return {'DOCKER_IMAGE_VERSION': version}
