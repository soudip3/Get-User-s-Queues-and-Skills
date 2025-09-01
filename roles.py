import requests,json
import time

def roleDetails(access_token, ENVIRONMENT, userId):
    request_headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.get(f"https://api.{ENVIRONMENT}/api/v2/authorization/subjects/{userId}?pageSize=99999",  headers=request_headers)
    response_json = response.json()
    time.sleep(0.3)
    return response_json