from django.conf import settings


def LokerHub(request):
    context = {}
    context.update({
        'SITE_DOMAIN': settings.SITE_DOMAIN,
        'CURRENT_URL': settings.SITE_DOMAIN + request.path,
        'GOOGLE_ANALYTIC_CODE': settings.GOOGLE_ANALYTIC_CODE,
    })
    return context
