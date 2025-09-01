import requests,json
import time

def getPhone(access_token, ENVIRONMENT, lineId):
    request_headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.get(f"https://api.{ENVIRONMENT}/api/v2/telephony/providers/edges/phones?lines.name={lineId}&pageNumber=1&pageSize=25&sortBy=name&sortOrder=asc",  headers=request_headers)
    response_json = response.json()
    time.sleep(0.3)
    return response_json