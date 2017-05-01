# -*- coding: utf-8 -*-
from __future__ import unicode_literals
try:
    from httplib import HTTPConnection, HTTPSConnection, OK, ACCEPTED
except ImportError:
    from http.client import HTTPConnection, HTTPSConnection, OK, ACCEPTED
import ssl
from base64 import b64encode, b64decode
import json
import logging
try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

from .errors import APIError, ConfigurationError

import sys
pyversion = sys.version_info[0]

class Response(object):
    def __init__(self, http_response):
        try:
            self.data = json.load(http_response)
        # If response contains no text, return the raw object
        except ValueError:
            self.data = http_response


class BaseYarnAPI(object):
    response_class = Response

    def request(self, api_path, action='GET', headers=None, body="", **query_args):
        params = urlencode(query_args)
        if params:
            path = api_path + '?' + params
        else:
            path = api_path

        self.logger.info('Request https://%s:%s%s', self.address, self.port, path)

        if(self.username and self.password):
            #we need to base 64 encode it
            #and then decode it to acsii as python 3 stores it as a byte string
            cred = '%s:%s' % (self.username, self.password)
            # if python 2.x bytes has no 'utf-8' flag
            if pyversion == 3:
                credentials = bytes(cred, 'utf-8')
            else:
                credentials = bytes(cred)
            print(credentials)
            userAndPass = b64encode(credentials).decode('ascii')
            print(userAndPass)
            print(b64decode(userAndPass))
            # update header if provided
            auth = { 'Authorization' : 'Basic %s' %  userAndPass }
            if headers: 
                headers.update(auth)
            else: 
                headers = auth
            print(headers)

        print(path)
        http_conn = self.http_conn
        http_conn.request(method=action, url=path, body=body, headers=headers)
        response = http_conn.getresponse()

        # ACCEPTED = 202: If the request has been accepted for processing
        if response.status == OK or response.status == ACCEPTED:
            return self.response_class(response)
        else:
            msg = 'Response finished with status: %s' % response.status
            raise APIError(msg)

    def construct_parameters(self, arguments):
        params = dict((key, value) for key, value in arguments if value is not None)
        return params

    @property
    def http_conn(self):
        if self.address is None:
            raise ConfigurationError('API address is not set')
        elif self.port is None:
            raise ConfigurationError('API port is not set')

        print('connecting to ' + self.address, self.port)
        return HTTPSConnection(self.address, self.port, timeout=self.timeout, context=ssl._create_unverified_context())

    __logger = None
    @property
    def logger(self):
        if self.__logger is None:
            self.__logger = logging.getLogger(self.__module__)
        return self.__logger
