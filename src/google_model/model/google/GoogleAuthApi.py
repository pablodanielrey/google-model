'''
    https://developers.google.com/admin-sdk/directory/
    https://developers.google.com/admin-sdk/directory/v1/reference/users/

    aca estan los scopes
    https://developers.google.com/identity/protocols/googlescopes


    librerias:
    https://developers.google.com/identity/protocols/oauth2/service-account
    https://github.com/googleapis/google-api-python-client
    https://googleapis.dev/python/google-auth
'''

import os

from googleapiclient import discovery, errors

from google.oauth2 import service_account
from google.auth import impersonated_credentials
from google.auth.transport.requests import AuthorizedSession

class GAuthApis:

    SCOPES = ['https://www.googleapis.com/auth/admin.directory.user']

    SCOPESGMAIL = [
        'https://mail.google.com/',
        'https://www.googleapis.com/auth/gmail.settings.sharing'
    ]

    """
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets',
              'https://www.googleapis.com/auth/drive']
    """

    def getCredentials(self, username, SCOPES=SCOPES):
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,'credentials.json')
        credentials = service_account.Credentials.from_service_account_file(credential_path, scopes=SCOPES)
        """
        de acuerdo a la libreria se debe hacer asi.
        admin_credentials = impersonated_credentials.Credentials(source_credentials=credentials, \
                                                                 target_principal=username, \
                                                                 target_scopes=SCOPES)
        """
        user_credentials = credentials.with_subject(username)
        return user_credentials

    def getService(self, version, api, scopes, username):
        credentials = self.getCredentials(username, scopes)
        service = discovery.build(api, version, credentials=credentials, cache_discovery=False)
        return service

    def getAdminService(self, username, version='directory_v1'):
        api='admin'
        return self.getService(version, api, self.SCOPES, username)

    def getGmailService(self, username, version='v1'):
        api='gmail'
        return self.getService(version, api, self.SCOPESGMAIL, username)

