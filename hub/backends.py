from django.contrib.auth.backends import ModelBackend

from hub.models import OneallToken

class OneallBackend(ModelBackend):

    def authenticate(self, oneall_token=None):
        try:
            token = OneallToken.objects.get(token=oneall_token)
        except OneallToken.DoesNotExist:
            return None
        else:
            return token.user
