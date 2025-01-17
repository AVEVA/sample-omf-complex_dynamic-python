
import requests
import time
import json
from urllib.parse import urlparse

from EndpointTypes import EndpointTypes


def get_token(endpoint):
    '''Gets the token for the omfendpoint'''

    endpoint_type = endpoint['EndpointType']
    # return an empty string if the endpoint is not a Cds type
    if endpoint_type != EndpointTypes.CDS:
        return ''

    if (('expiration' in endpoint) and (endpoint['expiration'] - time.time()) > 5 * 60):
        return endpoint["token"]

    # we can't short circuit it, so we must go retreive it.

    discovery_url = requests.get(
        endpoint['Resource'] + '/identity/.well-known/openid-configuration',
        headers={'Accept': 'application/json'},
        verify=endpoint['VerifySSL'])

    if discovery_url.status_code < 200 or discovery_url.status_code >= 300:
        discovery_url.close()
        raise Exception(f'Failed to get access token endpoint from discovery URL: {discovery_url.status_code}:{discovery_url.text}')

    token_endpoint = json.loads(discovery_url.content)['token_endpoint']
    token_url = urlparse(token_endpoint)
    # Validate URL
    assert token_url.scheme == 'https'
    assert token_url.geturl().startswith(endpoint['Resource'])

    token_information = requests.post(
        token_url.geturl(),
        data={'client_id': endpoint['ClientId'],
              'client_secret': endpoint['ClientSecret'],
              'grant_type': 'client_credentials'},
        verify=endpoint['VerifySSL'])

    token = json.loads(token_information.content)

    if token is None:
        raise Exception('Failed to retrieve Token')

    __expiration = float(token['expires_in']) + time.time()
    __token = token['access_token']

    # cache the results
    endpoint['expiration'] = __expiration
    endpoint['token'] = __token

    return __token


def get_auth_header(endpoint):

    if endpoint['EndpointType'] == EndpointTypes.CDS:
        return (f'Bearer {get_token(endpoint)}')
    else:
        return None


def sanitize_headers(headers):
    validated_headers = {}

    for key in headers:
        if key in {'authorization', 'messagetype', 'action', 'messageformat', 'omfversion', 'x-requested-with'}:
            validated_headers[key] = headers[key]

    return validated_headers
