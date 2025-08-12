import authentication
from openpyxl import Workbook
import getUsers
import getQueues
import getSkills


CLIENT_ID = ""
CLIENT_SECRET = ""
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
sheet["C1"] = "UserID"
sheet["D1"] = "Queues"
sheet["E1"] = "Skills"


while(repeat):
    # get users details
    userResponse = getUsers.userDeatils(access_token, ENVIRONMENT, pageNumber)
    for user in userResponse["results"]:
        name = user["name"]
        email = user["email"]
        id = user["id"]
        # get queue details by user id
        queueResponse = getQueues.queueDetails(access_token, ENVIRONMENT, user["id"])
        skillResponse = getSkills.skillDetails(access_token, ENVIRONMENT, user["id"])
        queueName = ""
        for queue in  queueResponse["entities"]:
            if(queueName != ""):
                queueName = queueName + ", " + queue["name"]
            else:
                queueName = queue["name"]
        skillName = ""
        for skill in  skillResponse["entities"]:
            if(skillName != ""):
                skillName = skillName + ", " + skill["name"]
            else:
                skillName = skill["name"]
        sheet[f"A{i}"] = name
        sheet[f"B{i}"] = email
        sheet[f"C{i}"] = id
        sheet[f"D{i}"] = queueName
        sheet[f"E{i}"] = skillName
        i += 1
        print(name)
        # print(f"Name: {name}, Email: {email}, ID: {id}, Queues: {queueName}")
    count = userResponse["total"]
    if(pageNumber*100 >= count):
        repeat = False
    else:
        pageNumber += 1
wb.save("Users.xlsx")
wb.close()