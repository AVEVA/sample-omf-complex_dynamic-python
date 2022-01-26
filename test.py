import json
import requests
import traceback
import time

import program
import sendOMF
import omfHelper
import auth
from EndpointTypes import EndpointTypes

config = {}


def suppress_error(call):
    try:
        call()
    except Exception as e:
        print(f'Encountered Error: {e}')


def check_data(endpoint):
    if endpoint["EndpointType"] == EndpointTypes.ADH:
        check_last_ocs_val(endpoint)
    # don't have to check others as they are sync and we get instant feedback on success from the app itself


def check_last_ocs_val(endpoint):
    time.sleep(10)
    msg_headers = auth.sanitize_headers({
        "authorization": auth.get_auth_header(endpoint)
    })
    url = endpoint['OmfEndpoint'].split('/omf')[0] + \
        '/streams/Tank1Measurements/data/last'
    response = requests.get(
        url,
        headers=msg_headers,
        verify=endpoint["VerifySSL"]
    )

    # response code in 200s if the request was successful!
    if response.status_code < 200 or response.status_code >= 300:
        print(msg_headers)
        response.close()
        print(
            f'Response from was bad.  message: {response.status_code} {response.text}.')
        print()
        raise Exception(
            f'OMF message was unsuccessful,  {response.status_code}:{response.text}')


def send_type_delete(endpoint, _type):
    sendOMF.send_call(endpoint, json.dumps(_type), 'type', 'delete')


def send_container_delete(endpoint, container):
    sendOMF.send_call(endpoint, json.dumps(container), 'container', 'delete')


def test_main():
    '''Tests to make sure the sample runs as expected'''
    
    endpoints = []
    try:
        endpoints, omf_version = program.main(True, ['2,3', 'n'])
        sendOMF.set_omf_version(omf_version)

        for endpoint in endpoints:
            if endpoint['Selected']:
                check_data(endpoint)

    except Exception as ex:
        print(f'Encountered Error: {ex}.')
        print
        traceback.print_exc()
        print
        raise ex

    finally:
        print('Deletes')
        print

        for endpoint in endpoints:
            if endpoint['Selected']:
                suppress_error(lambda: send_container_delete(endpoint, omfHelper.get_container()))
                suppress_error(lambda: send_type_delete(endpoint, omfHelper.get_type()))


if __name__ == '__main__':
    test_main()
