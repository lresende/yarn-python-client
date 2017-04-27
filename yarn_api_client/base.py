# -*- coding: utf-8 -*-
from __future__ import unicode_literals
try:
    from httplib import HTTPConnection, HTTPSConnection, OK
except ImportError:
    from http.client import HTTPConnection, HTTPSConnection, OK
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
        self.data = json.load(http_response)


class BaseYarnAPI(object):
    response_class = Response

    def request(self, api_path, **query_args):
        params = urlencode(query_args)
        if params:
            path = api_path + '?' + params
        else:
            path = api_path

        self.logger.info('Request https://%s:%s%s', self.address, self.port, path)

        headers = None
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
            headers = { 'Authorization' : 'Basic %s' %  userAndPass }
            print(headers)


        print(path)
        http_conn = self.http_conn
        http_conn.request('GET', path, headers=headers)
        response = http_conn.getresponse()

        if response.status == OK:
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
