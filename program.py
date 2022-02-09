# ************************************************************************
# Import necessary packages
# ************************************************************************

import json
import sys

import sendOMF
import omfHelper
from EndpointTypes import EndpointTypes


def get_json_file(filename):
    ''' Get a json file by the path specified relative to the application's path'''

    # Try to open the configuration file
    try:
        with open(
            filename,
            'r',
        ) as f:
            loaded_json = json.load(f)
    except Exception as error:
        print(f'Error: {str(error)}')
        print(f'Could not open/read file: {filename}')
        exit()

    return loaded_json


def get_appsettings():
    ''' Return the appsettings.json as a json object, while also populating base_endpoint, omf_endpoint, and default values'''

    # Try to open the configuration file
    appsettings = get_json_file('appsettings.json')
    endpoints = appsettings["Endpoints"]
    omf_version = appsettings["OMFVersion"]

    # for each endpoint construct the check base and OMF endpoint and populate default values
    for endpoint in endpoints:
        endpoint["EndpointType"] = EndpointTypes(endpoint["EndpointType"])
        endpoint_type = endpoint["EndpointType"]

        # If the endpoint is ADH
        if endpoint_type == EndpointTypes.ADH:
            base_endpoint = f'{endpoint["Resource"]}/api/{endpoint["ApiVersion"]}' + \
                f'/tenants/{endpoint["TenantId"]}/namespaces/{endpoint["NamespaceId"]}'

        # If the endpoint is EDS
        elif endpoint_type == EndpointTypes.EDS:
            base_endpoint = f'{endpoint["Resource"]}/api/{endpoint["ApiVersion"]}' + \
                f'/tenants/default/namespaces/default'

        # If the endpoint is PI
        elif endpoint_type == EndpointTypes.PI:
            base_endpoint = endpoint["Resource"]

        else:
            raise ValueError('Invalid endpoint type')

        omf_endpoint = f'{base_endpoint}/omf'

        # add the base_endpoint and omf_endpoint to the endpoint configuration
        endpoint["BaseEndpoint"] = base_endpoint
        endpoint["OmfEndpoint"] = omf_endpoint

        # check for optional/nullable parameters
        if 'VerifySSL' not in endpoint or endpoint["VerifySSL"] == None:
            endpoint["VerifySSL"] = True

        if 'UseCompression' not in endpoint or endpoint["UseCompression"] == None:
            endpoint["UseCompression"] = True

        if 'WebRequestTimeoutSeconds' not in endpoint or endpoint["WebRequestTimeoutSeconds"] == None:
            endpoint["WebRequestTimeoutSeconds"] = 30

    return endpoints, omf_version


def main(test=False, entries=[]):
    # Main program.  Seperated out so that we can add a test function and call this easily
    print('Welcome')
    endpoints, omf_version = get_appsettings()

    sendOMF.set_omf_version(omf_version)

    for endpoint in endpoints:
        if not endpoint['Selected']:
            continue

        sendOMF.send_type_create(endpoint, omfHelper.get_type())
        sendOMF.send_container_create(endpoint, omfHelper.get_container())

        while not test or len(entries) > 0:
            ans = None
            # can read entries fromt he command line here
            if len(entries) > 0:
                ans = entries.pop(0)
            else:
                ans = input('Enter pressure, temperature: n to cancel:')

            if ans == 'n':
                break

            split = ans.split(',')
            sendOMF.send_data_create(endpoint, omfHelper.get_data(
                pressure=float(split[0]), temperature=float(split[1])))

    return endpoints, omf_version


if __name__ == "__main__":
    sys.argv.pop()
    main(entries=sys.argv)
    print("done")
