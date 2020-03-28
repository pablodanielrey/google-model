"""
    https://developers.google.com/admin-sdk/directory/v1/quickstart/python
    https://developers.google.com/resources/api-libraries/documentation/admin/directory_v1/python/latest/
"""

import os
import datetime
import uuid
import logging
import json

from .GoogleAuthApi import GAuthApis


class SyncGoogleModel:

    def __init__(self):
        self.admin = os.environ.get('ADMIN_USER_GOOGLE','sistemas@econo.unlp.edu.ar')
        self.service = GAuthApis.getServiceAdmin(self.admin)

    def _get_google_uid(self, username):
        return f"{username}@econo.unlp.edu.ar"

    def sync_login(self, username, credentials):
        try:
            usr = self._get_google_uid(username)

            """ https://developers.google.com/resources/api-libraries/documentation/admin/directory_v1/python/latest/admin_directory_v1.users.html """
            self.service.users().get(userKey=usr).execute()
            datos = {}
            datos["changePasswordAtNextLogin"] = False
            datos['password'] = credentials
            r = self.service.users().update(userKey=usr,body=datos).execute()
            if not r.ok:
                raise Exception(r.response)

        except Exception as e:
           ''' el usuario no existe '''
           raise e
