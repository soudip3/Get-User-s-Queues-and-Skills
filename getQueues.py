import requests,json
import time

def queueDetails(access_token, ENVIRONMENT, id):
    request_headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.get(f"https://api.{ENVIRONMENT}/api/v2/users/{id}/queues?pageSize=500", headers=request_headers)
    response_json = response.json()
    time.sleep(0.3)
    return response_json