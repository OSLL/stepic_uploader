from allauth.socialaccount import app_settings
from allauth.socialaccount.providers.base import ProviderAccount
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider


class StepikAccount(ProviderAccount):
    def get_profile_url(self):
        return ('https://stepik.org/api/stepics/1')

    def to_str(self):
        first_name = self.account.extra_data.get('first_name', '')
        last_name = self.account.extra_data.get('last_name', '')
        name = ' '.join([first_name, last_name]).strip()
        return name or super(StepikAccount, self).to_str()
    #pass

class StepikProvider(OAuth2Provider):
    id = 'stepik'
    name = 'Stepik'
    account_class = StepikAccount

    def get_default_scope(self):
        scope = []
        if app_settings.QUERY_EMAIL:
            scope.append('email_addresses')
        return scope

    def extract_uid(self, data):
        return str(data[0]['id'])

    def extract_common_fields(self, data):
        return dict(#email=data[0].get('email_addresses'),
                    email='exaple@mail.ru',
                    last_name=data[0].get('last_name'),
                    username=data[0].get('full_name'),
                    first_name=data[0].get('first_name'))


provider_classes = [StepikProvider]
