import requests

from allauth.socialaccount.providers.oauth2.client import OAuth2Client

from django.utils.http import urlencode

#from allauth.compat import parse_qsl




class StepikOAuth2Client(OAuth2Client):

    def get_redirect_url(self, authorization_url, extra_params): #переадресация пользователя на сайт провайдера ДА
        params = {
            'client_id': self.consumer_key,
            'redirect_uri': self.callback_url,
         #   'scope': self.scope,
            'response_type': 'code'
        }
        if self.state:
            params['state'] = self.state
        params.update(extra_params)
        return '%s?%s' % (authorization_url, urlencode(params))

