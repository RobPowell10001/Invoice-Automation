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

#returns 0 for no errors, 1 for API errors, and 2 for viewhacking errors
def fixTaskCompletionOrder(projectNumber):
    statusCode = 0
    with open('./appsettings.json', 'r') as file:
        # Load the JSON data
        appsettings = json.load(file)


    print(projectNumber)

    # Get OAuth2 API Access in Python ✅
    headers = {
    'Authorization': f'Bearer {appsettings[f"{appsettings["mode"]}bearer"]}',
    }

    parameters = {
        'Sort':"DateUpdated"
    }

    # Find Project ID from Project Number (GET Project)
    response = requests.request("GET", "https://api.avaza.com/api/Project", headers=headers, params=parameters)
    if (response.status_code != 200 and (statusCode == 0 or statusCode == 2)):
                    statusCode+= 1

    json_data = response.text 

    # Parse the JSON string
    parsed_data = json.loads(json_data)


    projectID = ""
    targetString = f"{projectNumber} - "
    for project in parsed_data['Projects']:
        if project['Title'].startswith(targetString):
            projectID = project['ProjectID']
            break
    if projectID == "":
        return 4

    #print(projectID)
    # Use hacked view data to find proper task order (ViewDataRetriever)
    viewDataResponse = getViewData(projectID=projectID)
    projectViewData = viewDataResponse[0]
    viewDataSuccess = viewDataResponse[1]
    if not viewDataSuccess:
        statusCode += 2
         
    #find "Section 1 Group"
    for group in projectViewData['groups']:
        if "Section 1" in group['Title']:
            for task in group["tasks"]:
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
            break
    return statusCode



    # For each TaskID in viewdata, in viewdata order,
    #for task in projectViewData
    # Uncheck (PUT Task)
    # Recheck (PUT Task)
    # Problems:
    # Do we need 1 second delay between uncheck, recheck, and uncheck?


# main
# Take Project Number as input (input)✅