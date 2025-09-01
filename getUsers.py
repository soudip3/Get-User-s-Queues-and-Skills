import requests,json
import time

def userDeatils(access_token, ENVIRONMENT, pageNumber):
    request_headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    request_body = json.dumps({"pageSize":100,"pageNumber":pageNumber,"query":[{"type":"EXACT","fields":["state"],"values":["active","inactive"]}],"sortOrder":"ASC","sortBy":"name","expand":["images","authorization","team"],"enforcePermissions":True})

    response = requests.post(f"https://api.{ENVIRONMENT}/api/v2/users/search", data=request_body, headers=request_headers)
    response_json = response.json()
    time.sleep(0.3)
    return response_json

def userBasicInfo(access_token, ENVIRONMENT, userId):
    request_headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.get(f"https://api.{ENVIRONMENT}/api/v2/users/{userId}?expand=station,locations,skills,employerInfo&pageSize=999", headers=request_headers)
    response_json = response.json()
    time.sleep(0.3)
    return response_json