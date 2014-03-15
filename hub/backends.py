from django.contrib.auth.backends import ModelBackend

from hub.models import SocialLoginProvider
"""
{u'Email': [{u'Type': u'Primary', u'Value': u'ekaputra@balitechy.com'}], u'Suffix': None, u'FirstName': u'Eka', u'MiddleName': u'', u'LastName': u'Putra', u'ImageUrl': u'https://graph.facebook.com/100000145269859/picture?type=large', u'Country': None, u'BirthDate': u'7/14/1985', u'ThumbnailImageUrl': u'https://graph.facebook.com/100000145269859/picture?type=square', u'Prefix': None, u'Gender': u'M', u'Provider': u'facebook', u'LocalCountry': u'Indonesia', u'ProfileName': u'ekaputra07', u'FullName': u'Eka Putra', u'NickName': None, u'ID': u'100000145269859', u'ProfileCountry': None}
{u'Email': [{u'Type': u'Primary', u'Value': u'ekaputra07@gmail.com'}], u'Suffix': None, u'FirstName': u'Eka', u'MiddleName': None, u'LastName': u'Putra', u'ImageUrl': u'http://lh6.googleusercontent.com/-5ekxSaiIUEI/AAAAAAAAAAI/AAAAAAAAAQU/4JTpHUDcFDw/photo.jpg', u'Country': None, u'BirthDate': None, u'ThumbnailImageUrl': u'http://lh6.googleusercontent.com/-5ekxSaiIUEI/AAAAAAAAAAI/AAAAAAAAAQU/4JTpHUDcFDw/photo.jpg', u'Prefix': None, u'Gender': u'M', u'Provider': u'google', u'LocalCountry': u'Indonesia', u'ProfileName': None, u'FullName': u'Eka Putra', u'NickName': None, u'ID': u'115732862699314368137', u'ProfileCountry': None}
"""

class LoginRadiusBackend(ModelBackend):
    """
    Authentication backend that will only authenticate by social ID.
    This backend must only be used in conjunction with social login.
    This backend automatically create user with specified username if does not exist yet.
    """
    def authenticate(self, provider=None, provider_user_id=None):
        try:
            provider_user = SocialLoginProvider.objects.get(name=provider,
                                                            provider_user_id=provider_user_id)
        except SocialLoginProvider.DoesNotExist:
            return None
        else:
            return provider_user.user
