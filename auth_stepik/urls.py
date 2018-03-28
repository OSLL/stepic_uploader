from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns
from .provider import StepikProvider



urlpatterns = default_urlpatterns(StepikProvider)
