import authentication
from openpyxl import Workbook
import getUsers
import getQueues
import roles
import webRTC


CLIENT_ID = "963718db-af8e-4003-aa59-2a31301be20b"
CLIENT_SECRET = "JqVckgpDldMJMmxHivQV2fA8cgatncsgU_Vr_hFQcrE"
ENVIRONMENT = "usw2.pure.cloud" # eg. mypurecloud.com


#get token
access_token = authentication.authentication(CLIENT_ID, CLIENT_SECRET, ENVIRONMENT)


repeat = True
pageNumber = 1
i=2
wb = Workbook()
sheet = wb.active
sheet["A1"] = "Name"
sheet["B1"] = "Email"
sheet["C1"] = "Division"
sheet["D1"] = "Roles"
sheet["E1"] = "Queues"
sheet["F1"] = "Skills"
sheet["G1"] = "WebRTC"
sheet["H1"] = "Work Phone"
sheet["I1"] = "Work Phone 2"


while(repeat):
    # get users details
    userResponse = getUsers.userDeatils(access_token, ENVIRONMENT, pageNumber)
    for user in userResponse["results"]:
        name = user["name"]
        print(name)
        email = user["email"]
        id = user["id"]
        # get queue details by user id
        queueResponse = getQueues.queueDetails(access_token, ENVIRONMENT, user["id"])
        queueName = ""
        for queue in  queueResponse["entities"]:
            if(queueName != ""):
                queueName = queueName + ", " + queue["name"]
            else:
                queueName = queue["name"]
        userBasicInfoResponse = getUsers.userBasicInfo(access_token, ENVIRONMENT, id)
        division = userBasicInfoResponse["division"]["name"]
        try:    
            if(userBasicInfoResponse["addresses"][0]["display"] != ""):
                workPhone = userBasicInfoResponse["addresses"][0]["display"]
        except IndexError:
            workPhone = ""
        try:
            workPhone2 = userBasicInfoResponse["addresses"][1]["display"]
        except IndexError:
            workPhone2 = ""
        try:    
            if(userBasicInfoResponse["station"]["associatedStation"]["providerInfo"]["name"] != ""):
                lineId = userBasicInfoResponse["station"]["associatedStation"]["providerInfo"]["name"]
        except KeyError:
            lineId = ""
        skillName = ""
        for skill in  userBasicInfoResponse["skills"]:
            if(skillName != ""):
                skillName = skillName + ", " + skill["name"]
            else:
                skillName = skill["name"]
        roleResponse = roles.roleDetails(access_token, ENVIRONMENT, id)
        roleName = ""
        for role in roleResponse["grants"]:
            if role["division"]["id"] == "*":
                roleDivision = "All Division"
            else:
                roleDivision = role["division"]["name"]
            if(roleName != ""):
                roleName = roleName + ", " + role["role"]["name"] + "-" + roleDivision
            else:
                roleName = role["role"]["name"] + "-" + roleDivision
        if lineId!="":
            try:
                webRTCResponse = webRTC.getPhone(access_token, ENVIRONMENT, lineId)
                webRTCName = webRTCResponse["entities"][0]["name"]
            except IndexError:
                webRTCName = ""
        else:
            webRTCName = ""
        sheet[f"A{i}"] = name
        sheet[f"B{i}"] = email
        sheet[f"C{i}"] = division
        sheet[f"G{i}"] = webRTCName
        sheet[f"D{i}"] = roleName
        sheet[f"H{i}"] = workPhone
        sheet[f"I{i}"] = workPhone2
        sheet[f"E{i}"] = queueName
        sheet[f"F{i}"] = skillName
        i += 1
        # print(f"Name: {name}, Email: {email}, ID: {id}, Queues: {queueName}")
    count = userResponse["total"]
    if(pageNumber*100 >= count):
        repeat = False
    else:
        pageNumber += 1
wb.save("Users.xlsx")
wb.close()