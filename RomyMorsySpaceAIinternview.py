import requests
import scaleapi
import numpy as np
import pandas as pd
import os
import json
import pprint
pp = pprint.PrettyPrinter(indent=4)


def myCheck(annotation):
    '''Check to be implemented:
    if an object has occlusion of 50% and a backgroud color of not_applicable
    that will be thrown a warning and if the occlusion is over 75% and the
    background_color is not_applicable then we will throw an error on it'''

    attributes = annotation['attributes']
    occlusion =  float(attributes['occlusion'][:-1])
    background_color = attributes['background_color']
    if occlusion == 50.0 and background_color == 'not_applicable':
        return 'warning' #: object is not fully visible and may be a non-visible face'
    if occlusion >= 75.0 and background_color == 'not_applicable':
        return 'error' #: object is not visible and may be a non-visible face'
    else:
        return 'no issue'

#### Initialize values for API authentication
API_KEY = os.getenv('MY_TOKEN','Token not found')
client = scaleapi.ScaleClient(API_KEY)
url = "https://api.scale.com/v1/tasks"
querystring = { "project": "Traffic Sign Detection" }
headers = {
    "Accept": "application/json",
    "Authorization": "Basic bGl2ZV83NDI3NWI5YjJiOGI0NGQ4YWQxNTZkYjAzZDIwMDhlZDo="
}


####Making our API call
response = requests.request(
    "GET",url,
    headers=headers,
    auth=(API_KEY, ''),
    params=querystring
)
data = response.json()

task_dict = {}
for task in data['docs']:
    task_id = task['task_id']
    annotations = task['response']['annotations']

    annotation_dict = {}
    for annotation in annotations:
        check = myCheck(annotation)
        #Check for errors and warnings and only pass those
        if (check == 'error' or check == 'warning'):
            annotation_dict[annotation['uuid']] = check

    if(len(annotation_dict.keys())):
        task_dict[task_id] = annotation_dict


pp.pprint(task_dict)

#Write to a json file for output
with open('output.json','w') as json_file:
    json.dump(task_dict,json_file)
json_file.close()
