import base64, sys, os
import requests,json

def authentication(CLIENT_ID, CLIENT_SECRET, ENVIRONMENT):
    # Base64 encode the client ID and client secret
    authorization = base64.b64encode(bytes(CLIENT_ID + ":" + CLIENT_SECRET, "ISO-8859-1")).decode("ascii")

    # Prepare for POST /oauth/token request
    request_headers = {
        "Authorization": f"Basic {authorization}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    request_body = {
        "grant_type": "client_credentials"
    }


    # Get token
    response = requests.post(f"https://login.{ENVIRONMENT}/oauth/token", data=request_body, headers=request_headers)

    # Check response
    if response.status_code != 200:
        print(f"Failure: { str(response.status_code) } - { response.reason }")
        sys.exit(response.status_code)

    # Get JSON response body
    response_json = response.json()
    access_token = response_json["access_token"]
    return access_token