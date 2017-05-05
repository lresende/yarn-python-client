try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse

class Uri:

    def __init__(self, uri):
        parsedUri = urlparse(uri)
        self.scheme = parsedUri.scheme
        self.netloc = parsedUri.netloc
        self.path = parsedUri.path
        self.params = parsedUri.params
        self.query = parsedUri.query
        self.username = parsedUri.username
        self.password = parsedUri.password
        self.hostname = parsedUri.hostname
        self.port = parsedUri.port