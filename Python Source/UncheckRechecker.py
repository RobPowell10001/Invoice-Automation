import requests 
import json
import webbrowser

#returns JSON parsed view data
def getViewData(projectID):

  with open('./appsettings.json', 'r') as file:
      # Load the JSON data
      appsettings = json.load(file)

  url = f"{appsettings[f"{appsettings["mode"]}endpoint"]}{projectID}{appsettings[f"{appsettings["mode"]}grouping"]}"

  payload = {}
  headers = {
    'cookie': f'.AspNet.ApplicationCookie={appsettings[f"{appsettings["mode"]}cookie"]};',
  }

  response = requests.request("GET", url, headers=headers, data=payload)
  success = (response.status_code == 200)

  json_data =response.text 

  # Parse the JSON string
  parsed_data = json.loads(json_data)

  return [parsed_data, success]

# returns:
# ProjectID for no errors
# -1 for couldn't find
def projectNumberToProjectID(projectNumber):
    with open('./appsettings.json', 'r') as file:
        # Load the JSON data
        appsettings = json.load(file)

    # Get OAuth2 API Access in Python ✅
    headers = {
    'Authorization': f'Bearer {appsettings[f"{appsettings["mode"]}bearer"]}',
    }

    parameters = {
        'Sort':"DateUpdated desc",
        "pageSize":1000
    }

    # Find Project ID from Project Number (GET Project)
    response = requests.request("GET", "https://api.avaza.com/api/Project", headers=headers, params=parameters)

    json_data = response.text 
    print(json_data)

    # Parse the JSON string
    parsed_data = json.loads(json_data)


    projectID = "-1"
    targetString = f"{projectNumber} - "
    title = ""
    for project in parsed_data['Projects']:
        if project['Title'].startswith(targetString):
            projectID = project['ProjectID']
            title = project['Title']
            break
    if(projectID != "-1"):
        return [projectID, title]
    else:
        return [projectID, "Error, Project Not Found"]

#returns:
# 0 for no errors
# 1 for API errors
# 2 for viewhacking errors
# 3 for API and viewhacking errors
# 4 for couldnt find projectNumber
def fixTaskCompletionOrder(projectID):
    statusCode = 0

    with open('./appsettings.json', 'r') as file:
        # Load the JSON data
        appsettings = json.load(file)

    # Get OAuth2 API Access in Python ✅
    headers = {
    'Authorization': f'Bearer {appsettings[f"{appsettings["mode"]}bearer"]}',
    }
    #print(projectID)
    # Use hacked view data to find proper task order (ViewDataRetriever)
    viewDataResponse = getViewData(projectID=projectID)
    projectViewData = viewDataResponse[0]
    viewDataSuccess = viewDataResponse[1]
    if not viewDataSuccess:
        statusCode += 2
         
    #find "Section 1 Group"
    for group in projectViewData['groups']:
        for task in group["tasks"]:
            print(f"editing Task {task["Title"]}")
            model = { 
                    "TaskID": f"{task["TaskID"]}",
                    "FieldsToUpdate": ["TaskStatusCode"],
                    "TaskStatusCode": "NotStarted",
                }
            response = requests.request("PUT", "https://api.avaza.com/api/Task", headers=headers, json=model)
            if (response.status_code != 200 and (statusCode == 0 or statusCode == 2)):
                statusCode+= 1
            model = { 
                    "TaskID": f"{task["TaskID"]}",
                    "FieldsToUpdate": ["TaskStatusCode"],
                    "TaskStatusCode": "Complete",
                }
            response = requests.request("PUT", "https://api.avaza.com/api/Task", headers=headers, json=model)
            if (response.status_code != 200 and (statusCode == 0 or statusCode == 2)):
                statusCode+= 1
    return statusCode



    # For each TaskID in viewdata, in viewdata order,
    #for task in projectViewData
    # Uncheck (PUT Task)
    # Recheck (PUT Task)
    # Problems:
    # Do we need 1 second delay between uncheck, recheck, and uncheck?


# main
# Take Project Number as input (input)✅