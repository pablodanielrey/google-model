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

class UserNotFoundException(Exception):
    pass

class SyncGoogleModel:

    def __init__(self):
        self.admin = os.environ.get('ADMIN_USER_GOOGLE','sistemas@econo.unlp.edu.ar')
        authApi = GAuthApis()
        self.service = authApi.getAdminService(self.admin)

    def _get_google_uid(self, username):
        return f"{username}@econo.unlp.edu.ar"

    def sync_login(self, username, credentials):
        try:
            # pylint: disable=no-member
            usr = self._get_google_uid(username)

            """ https://developers.google.com/resources/api-libraries/documentation/admin/directory_v1/python/latest/admin_directory_v1.users.html """
            self.service.users().get(userKey=usr).execute()
            datos = {}
            datos["changePasswordAtNextLogin"] = False
            datos['password'] = credentials
            r = self.service.users().update(userKey=usr,body=datos).execute()
            if not r:
                print(r.response)
                raise Exception(r.response)

        except Exception as e:
            try:
                # pylint: disable=no-member
                error = json.loads(e.content)
                if error['error']['code'] == 404:
                    ''' el usuario no existe '''
                    print(f"El usuario {username} no existe dentro de google")
                    raise UserNotFoundException(username)
            except UserNotFoundException as e1:
                raise e1
            except Exception as e1:
                raise e1
            raise e
