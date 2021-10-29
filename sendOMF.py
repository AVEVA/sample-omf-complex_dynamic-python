import requests
import json
import auth
from EndpointTypes import EndpointTypes

omf_version = '1.1'

def set_omf_version(version):
    global omf_version
    omf_version = version

def send_container_create(endpoint, container):
    send_call(endpoint, json.dumps(container), 'container', 'create')


def send_type_create(endpoint, _type):
    send_call(endpoint, json.dumps(_type), 'type', 'create')


def send_data_create(endpoint, data):
    send_call(endpoint, json.dumps(data), 'data', 'create')


def send_call(endpoint, msg_body, message_type, action):
    headers = auth.sanitize_headers(get_headers(endpoint, message_type, action))
    id_pwd = None
    if endpoint["EndpointType"] == EndpointTypes.PI:
        id_pwd = (endpoint['Username'], endpoint['Password'])

    response = requests.post(
        endpoint['OmfEndpoint'],
        headers=headers,
        data=msg_body,
        verify=endpoint['VerifySSL'],
        timeout=endpoint['WebRequestTimeoutSeconds'],
        auth=id_pwd
    )

    # Check for 409, which indicates that a type with the specified ID and version already exists.
    if response.status_code == 409:
        return

    # response code in 200s if the request was successful!
    if response.status_code < 200 or response.status_code >= 300:
        print(headers)
        response.close()
        print('Response from was bad.  "{0}" message: {1} {2}.  Message holdings: {3}'.format(
            message_type, response.status_code, response.text, msg_body))
        print()
        raise Exception("OMF message was unsuccessful, {message_type}. {status}:{reason}".format(
            message_type=message_type, status=response.status_code, reason=response.text))


def get_headers(endpoint, message_type, action):
    global omf_version

    msg_headers = {
        "x-requested-with": "xmlhttprequest",
        'messagetype': message_type,
        'action': action,
        'messageformat': 'JSON',
        'omfversion': omf_version
    }
    if endpoint['UseCompression'] == "gzip":
        msg_headers["compression"] = "gzip"

    authorization = auth.get_auth_header(endpoint)
    if authorization:
        msg_headers["authorization"] = authorization
    return msg_headers
