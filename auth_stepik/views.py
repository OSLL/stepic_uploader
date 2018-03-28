import requests
import json
from allauth.socialaccount.providers.oauth2.views import (
    OAuth2Adapter,
    OAuth2CallbackView,
    OAuth2LoginView,
    OAuth2View,
)

from allauth.socialaccount.providers.oauth2.client import (
  #  OAuth2Client,
    OAuth2Error,
)
from django.http import HttpResponseRedirect
from allauth.socialaccount.providers.base import AuthAction, AuthError
from .provider import StepikProvider
from .client import StepikOAuth2Client



class StepikOAuth2Adapter(OAuth2Adapter):
    provider_id = StepikProvider.id
    access_token_url = 'https://stepik.org/oauth2/token/'
    authorize_url = 'https://stepik.org/oauth2/authorize/'
    profile_url = 'https://stepik.org/api/stepics/1'

    def complete_login(self, request, app, token, **kwargs): 
        resp = json.loads(requests.get('https://stepik.org/api/stepics/1', headers={'Authorization': 'Bearer '+ token.token}).text)
        #user = resp['users']
        #name = user[0]['first_name'] +' ' + user[0]['last_name']
        extra_data=resp['users']
   
        return self.get_provider().sociallogin_from_response(request,
                                                             extra_data)
  
        

class StepikOAuth2View(OAuth2View):
    def get_client(self, request, app):
        callback_url = self.adapter.get_callback_url(request, app)
        provider = self.adapter.get_provider()
        scope = provider.get_scope(request)
        client = StepikOAuth2Client(self.request, app.client_id, app.secret,
                              self.adapter.access_token_method,
                              self.adapter.access_token_url,
                              callback_url,
                              scope,
                              scope_delimiter=self.adapter.scope_delimiter,
                              headers=self.adapter.headers,
                              basic_auth=self.adapter.basic_auth)
        return client                
                
class StepikOAuth2LoginView(StepikOAuth2View):
    def dispatch(self, request):
        provider = self.adapter.get_provider()
        app = provider.get_app(self.request)
        client = self.get_client(request, app)
        action = request.GET.get('action', AuthAction.AUTHENTICATE)
        auth_url = self.adapter.authorize_url
        auth_params = provider.get_auth_params(request, action)
        #client.state = SocialLogin.stash_state(request)
        try:
            return HttpResponseRedirect(client.get_redirect_url(
                auth_url, auth_params))
        except OAuth2Error as e:
            return render_authentication_error(
                request,
                provider.id,
                exception=e)

                
oauth2_login = StepikOAuth2LoginView.adapter_view(StepikOAuth2Adapter)
oauth2_callback = OAuth2CallbackView.adapter_view(StepikOAuth2Adapter)
