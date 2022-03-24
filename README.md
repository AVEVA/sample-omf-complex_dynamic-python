# Complex Dynamic OMF Python Sample

| :loudspeaker: **Notice**: Samples have been updated to reflect that they work on AVEVA Data Hub. The samples also work on OSIsoft Cloud Services unless otherwise noted. |
| -----------------------------------------------------------------------------------------------|  

**Version:** 1.2.2

---

| ADH Test Status                                                                                                                                                                                                                                                                                                                                                                      | EDS Test Status                                                                                                                                                                                                                                                                                                                                                                      | PI Test Status                                                                                                                                                                                                                                                                                                                                                                      |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [![Build Status](https://dev.azure.com/osieng/engineering/_apis/build/status/product-readiness/OMF/aveva.sample-omf-complex_dynamic-python?branchName=main&jobName=Tests_ADH)](https://dev.azure.com/osieng/engineering/_build/latest?definitionId=2640&branchName=main) | [![Build Status](https://dev.azure.com/osieng/engineering/_apis/build/status/product-readiness/OMF/aveva.sample-omf-complex_dynamic-python?branchName=main&jobName=Tests_EDS)](https://dev.azure.com/osieng/engineering/_build/latest?definitionId=2640&branchName=main) | [![Build Status](https://dev.azure.com/osieng/engineering/_apis/build/status/product-readiness/OMF/aveva.sample-omf-complex_dynamic-python?branchName=main&jobName=Tests_PI)](https://dev.azure.com/osieng/engineering/_build/latest?definitionId=2640&branchName=main) |

---

This sample uses OSIsoft Message Format to send data to AVEVA Data Hub, Edge Data Store, or PI Web API.

## Details

See [ReadMe](https://github.com/osisoft/OSI-Samples-OMF/blob/main/docs/COMPLEX_DYNAMIC_README.md)

## OSIsoft Message Format Endpoints

The sample is configured using the file [appsettings.placeholder.json](appsettings.placeholder.json). Before editing, rename this file to `appsettings.json`. This repository's `.gitignore` rules should prevent the file from ever being checked in to any fork or branch, to ensure credentials are not compromised.

Configure desired OMF endpoints to receive the data in `appsettings.json`. Only one of PI, EDS, or ADH can be configured at a time. This script was designed against OMF version 1.1.

## To Run this Sample:

1. Clone the GitHub repository
1. Install required modules: `pip install -r requirements.txt`
1. Open the folder with your favorite IDE
1. Rename the placeholder config file [appsettings.placeholder.json](appsettings.placeholder.json) to appsettings.json
1. Update appsettings.json with the credentials for the enpoint(s) you want to send to. See [Configure endpoints and authentication](#configure-endpoints-and-authentication) below for additional details
1. Run program.py

## To Test this Sample:

### Option 1

1. Run test.py

### Option 2

1. Install pytest `pip install pytest`
1. Run `pytest program.py`

## Configure Endpoints and Authentication

The sample is configured using the file [appsettings.placeholder.json](appsettings.placeholder.json). Before editing, rename this file to `appsettings.json`. This repository's `.gitignore` rules should prevent the file from ever being checked in to any fork or branch, to ensure credentials are not compromised.

The application can be configured to send to any number of endpoints specified in the endpoints array within appsettings.json. In addition, there are three types of endpoints: [ADH](#adh-endpoint-configuration), [EDS](#eds-endpoint-configuration), and [PI](#pi-endpoint-configuration). Each of the 3 types of enpoints are configured differently and their configurations are explained in the sections below.

### ADH Endpoint Configuration

An OMF ingress client must be configured. On our [AVEVA Learning](https://www.youtube.com/channel/UC333r4jIeHaY-rGgMjON54g) Channel on YouTube we have a video on [Creating an OMF Connection](https://www.youtube.com/watch?v=52lAnkGC1IM).

The format of the configuration for an ADH endpoint is shown below along with descriptions of each parameter. Replace all parameters with appropriate values.

```json
{
  "Selected": true,
  "EndpointType": "ADH",
  "Resource": "https://uswe.datahub.connect.aveva.com",
  "NamespaceId": "PLACEHOLDER_REPLACE_WITH_NAMESPACE_ID",
  "Tenant": "PLACEHOLDER_REPLACE_WITH_TENANT_ID",
  "clientId": "PLACEHOLDER_REPLACE_WITH_CLIENT_ID",
  "ClientSecret": "PLACEHOLDER_REPLACE_WITH_CLIENT_SECRET",
  "ApiVersion": "v1",
  "VerifySSL": true,
  "UseCompression": false,
  "WebRequestTimeoutSeconds": 30
}
```

| Parameters               | Required | Type    | Description                                                                                                                                                      |
| ------------------------ | -------- | ------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Selected                 | required | boolean | Tells the application if the endpoint should be sent to                                                                                                          |
| EndpointType             | required | string  | The endpoint type. For ADH this will always be "ADH"                                                                                                             |
| Resource                 | required | string  | The endpoint for ADH if the namespace. If the tenant/namespace is located in NA, it is https://uswe.datahub.connect.aveva.com and if in EMEA, it is https://euno.datahub.connect.aveva.com  |
| NamespaceID              | required | string  | The name of the Namespace in ADH that is being sent to                                                                                                           |
| Tenant                   | required | string  | The Tenant ID of the Tenant in ADH that is being sent to                                                                                                         |
| ClientId                 | required | string  | The client ID that is being used for authenticating to ADH                                                                                                       |
| ClientSecret             | required | string  | The client secret that is being used for authenticating to ADH                                                                                                   |
| ApiVersion               | required | string  | The API version of the ADH endpoint                                                                                                                              |
| VerifySSL                | optional | boolean | A feature flag for verifying SSL when connecting to the ADH endpoint. By defualt this is set to true as it is strongly recommended that SSL be checked           |
| UseCompression           | optional | boolean | A feature flag for enabling compression on messages sent to the ADH endpoint                                                                                     |
| WebRequestTimeoutSeconds | optional | integer | A feature flag for changing how long it takes for a request to time out                                                                                          |

### EDS Endpoint Configurations

The format of the configuration for an EDS endpoint is shown below along with descriptions of each parameter. Replace all parameters with appropriate values.

```json
{
  "Selected": true,
  "EndpointType": "EDS",
  "Resource": "http://localhost:5590",
  "ApiVersion": "v1",
  "UseCompression": false
}
```

| Parameters               | Required | Type    | Description                                                                                                                                       |
| ------------------------ | -------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| Selected                 | required | boolean | Tells the application if the endpoint should be sent to                                                                                           |
| EndpointType             | required | string  | The endpoint type. For EDS this will always be "EDS"                                                                                              |
| Resource                 | required | string  | The endpoint for EDS if the namespace. If EDS is being run on your local machine with the default configuration, it will be http://localhost:5590 |
| ApiVersion               | required | string  | The API version of the EDS endpoint                                                                                                               |
| UseCompression           | optional | boolean | A feature flag for enabling compression on messages sent to the ADH endpoint                                                                      |
| WebRequestTimeoutSeconds | optional | integer | A feature flag for changing how long it takes for a request to time out                                                                           |

### PI Endpoint Configuration

The format of the configuration for a PI endpoint is shown below along with descriptions of each parameter. Replace all parameters with appropriate values.

```json
{
  "Selected": true,
  "EndpointType": "PI",
  "Resource": "PLACEHOLDER_REPLACE_WITH_PI_WEB_API_URL",
  "DataArchiveName": "PLACEHOLDER_REPLACE_WITH_DATA_ARCHIVE_NAME",
  "Username": "PLACEHOLDER_REPLACE_WITH_USERNAME",
  "Password": "PLACEHOLDER_REPLACE_WITH_PASSWORD",
  "VerifySSL": true,
  "UseCompression": false
}
```

| Parameters               | Required | Type           | Description                                                                                                                                                                                                                                                                             |
| ------------------------ | -------- | -------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Selected                 | required | boolean        | Tells the application if the endpoint should be sent to                                                                                                                                                                                                                                 |
| EndpointType             | required | string         | The endpoint type. For PI this will always be "PI"                                                                                                                                                                                                                                      |
| Resource                 | required | string         | The URL of the PI Web API                                                                                                                                                                                                                                                               |
| DataArchiveName          | required | string         | The name of the PI Data Archive that is being sent to                                                                                                                                                                                                                                   |
| Username                 | required | string         | The username that is being used for authenticating to the PI Web API                                                                                                                                                                                                                    |
| Password                 | required | string         | The password that is being used for authenticating to the PI Web API                                                                                                                                                                                                                    |
| VerifySSL                | optional | boolean/string | A feature flag for verifying SSL when connecting to the PI Web API. Alternatively, this can specify the path to a .pem certificate file if a self-signed certificate is being used by the PI Web API. By defualt this is set to true as it is strongly recommended that SSL be checked. |
| UseCompression           | optional | boolean        | A feature flag for enabling compression on messages sent to the ADH endpoint                                                                                                                                                                                                            |
| WebRequestTimeoutSeconds | optional | integer        | A feature flag for changing how long it takes for a request to time out                                                                                                                                                                                                                 |

---
For the main OMF Complex Dynamic samples page [ReadMe](https://github.com/osisoft/OSI-Samples-OMF/blob/main/docs/COMPLEX_DYNAMIC.md)  
For the main OMF samples page [ReadMe](https://github.com/osisoft/OSI-Samples-OMF)  
For the main AVEVA samples page [ReadMe](https://github.com/osisoft/OSI-Samples)
