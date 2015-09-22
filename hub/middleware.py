from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


class IncompleteSignupMiddleware(object):
    """
    A middleware to check current loggin user has finished signup with valid email address.
    If still using generated email, redirect to finish signup page.
    """
    def process_request(self, request):
        path = request.path

        if path == '/logout/':
          return None

        user = request.user

        if user.is_authenticated():
            if ('+generated@lokerhub.com' in user.email) and path != '/finish-signup/':
                return HttpResponseRedirect(reverse('finish_signup'))
        return None

