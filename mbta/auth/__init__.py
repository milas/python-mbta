from .querystring import QueryStringAuth


class MbtaAuth(QueryStringAuth):
    def __init__(self, api_key: str):
        super().__init__(api_key=api_key)
