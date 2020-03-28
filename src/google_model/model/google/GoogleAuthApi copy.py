'''
    https://developers.google.com/admin-sdk/directory/
    https://developers.google.com/admin-sdk/directory/v1/reference/users/

    aca estan los scopes
    https://developers.google.com/identity/protocols/googlescopes
'''
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


class GAuthApis:

    SCOPES = 'https://www.googleapis.com/auth/admin.directory.user'

    SCOPESGMAIL = [
        'https://mail.google.com/',
        'https://www.googleapis.com/auth/gmail.settings.sharing'
    ]


    @classmethod
    def getCredentials(cls, username, SCOPES=SCOPES):
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        token_path = os.path.join(credential_dir, 'token.pickle')
        credential_path = os.path.join(credential_dir,'credentials.json')

        """Shows basic usage of the Admin SDK Directory API.
        Prints the emails and names of the first 10 users in the domain.
        """
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(token_path):
            with open(token_path, 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(credential_path, SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(token_path, 'wb') as token:
                pickle.dump(creds, token)

        ''' genera las credenciales delegadas al usuario username '''
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,'credentials.json')

        credentials = ServiceAccountCredentials.from_json_keyfile_name(credential_path, SCOPES)

        ''' uso una cuenta de admin del dominio para acceder a todas las apis '''
        admin_credentials = credentials.create_delegated(username)

        return admin_credentials

    @classmethod
    def getService(cls, version, api, scopes, username):
        credentials = cls.getCredentials(username, scopes)
        http = credentials.authorize(httplib2.Http())
        service = discovery.build(api, version, http=http, cache_discovery=False)
        return service

    @classmethod
    def getServiceAdmin(cls, username, version='directory_v1'):
        api='admin'
        return cls.getService(version, api, cls.SCOPES, username)

    @classmethod
    def getServiceGmail(cls, username, version='v1'):
        api='gmail'
        return cls.getService(version, api, cls.SCOPESGMAIL, username)

