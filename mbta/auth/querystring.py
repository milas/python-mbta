"""
Requests' authenticator that attaches given parameters
to the URL query string.

Source: https://gist.github.com/Xion/9c1bbbc287d4443dbaf5
        http://xion.io/post/code/requests-query-string-auth.html

"""
import requests.auth


class QueryStringAuth(requests.auth.AuthBase):
    """Authenticator that attaches a set of query string parameters
    (e.g. an API key) to the request.
    """
    def __init__(self, **params):
        self.params = {}
        for name, value in params.items():
            if value is None:
                continue  # None means 'no value' in Requests, too
            if name.endswith('[]'):
                name = name[:-2]
            self.params[name] = value

    def __call__(self, request: requests.PreparedRequest):
        if self.params:
            request.prepare_url(request.url, self.params)
        return request
