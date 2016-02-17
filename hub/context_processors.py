import datetime
from django.conf import settings
from django.core.urlresolvers import reverse


def LokerHub(request):
    context = {}
    context.update({
        'PREMIUM_FEE': settings.PREMIUM_FEE,
        'SITE_DOMAIN': settings.SITE_DOMAIN,
        'CURRENT_URL': settings.SITE_DOMAIN + request.path,
        'GOOGLE_ANALYTIC_CODE': settings.GOOGLE_ANALYTIC_CODE,
        'ONEALL_LOGIN_CALLBACK_URL': reverse('login_callback'),
        'NOW': datetime.datetime.now(),
    })
    return context
