from django.conf import settings


def LokerHub(request):
    context = {}
    context.update({
        'SITE_DOMAIN': settings.SITE_DOMAIN,
        'CURRENT_URL': settings.SITE_DOMAIN + request.path,
    })
    return context
