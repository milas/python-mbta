import os

import jsonapi_requests

from mbta.auth import MbtaAuth

config = jsonapi_requests.orm.OrmApi.config({
    'API_ROOT': 'https://api-v3.mbta.com',
    'APPEND_SLASH': False,
    'AUTH': MbtaAuth(api_key=os.environ.get('MBTA_API_KEY_V3', None))
})
