import requests 
import json

projectID = 291300

with open('secrets.json', 'r') as file:
    # Load the JSON data
    secrets = json.load(file)

url = f"{secrets["endpoint"]}{projectID}{secrets["grouping"]}"

payload = {}
headers = {
  'cookie': f'.AspNet.ApplicationCookie={secrets["cookie"]};',
}

response = requests.request("GET", url, headers=headers, data=payload)

json_data =response.text 

# Parse the JSON string
parsed_data = json.loads(json_data)

for task in parsed_data['groups'][1]['tasks']:
    print(task['Title'])
    print("\n")


