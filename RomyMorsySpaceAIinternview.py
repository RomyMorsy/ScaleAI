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

#task_dict = {key:val for key, val in task_dict.items() for k in val if val =='None'}
#for key,val in task_dict.items():
#    print('---------------------')
    #pp.pprint(task_dict.items())

    #for k in val:
        #pp.pprint(val[k])
    #    pp.pprint(task_dict[key])
    #    if task_dict[key].values() == 'None':
         #  pp.print(task_dict)


pp.pprint(task_dict)

#Write to a json file for output
with open('output.json','w') as json_file:
    json.dump(task_dict,json_file)
json_file.close()


    #print(len_tasks)
    #print(data['docs'][0]['response']['annotations'])
    #len_objects = len(data['docs'][0]['response']['annotations'])
    #print(len_objects)
### Loop through the tasks to obtain the number of objects that are annotated in each one
# for i in range(0,len_tasks):
#     objects.append(data['docs'][i])
#
# print(len_objects)
### Loop through each task and retrieve the info of every annotated object for each task
#print(objects[7])
#sort json

#print(objects[7]['response']['annotations'][19])

#picking up the task_ids for every record as well as the amount of annotated images per task
# for k in range(0,len_tasks):
#      #print(objects[k]['task_id'])
#      #print('---------------------------------------')
#      len_objects.append(len(objects[k]['response']['annotations']))
#      #print(len_objects[k])
     #print(objects[k]['response']['annotations'][1])
#print(objects[0]['task_id'])
#print(objects[0]['response']['annotations'][12])
#print(len_objects[0])
#for i in range(0,len_tasks):
    #for k in len_objects:
    #     print(k)
    #     print(i)
        # print(objects[i]['response']['annotations'][k])

    # return annotation['attributes']
# print(myCheck(objects[0]['response']['annotations']))
#print(sorted_objects)
#for object in sorted_objects:

    #print(object['response']['annotations'])
    #print("---------------------------------------------------")
    #len_objects.append(len(object['response']['annotations']))
    #print(len_objects)

    #annotations.append(object['response']['annotations'])
    #print(annotations)

    #print("---------------------------------------------------")
    #print(annotations[-1])


        #print(data['docs'][i]['response']['annotations'][k])













####Loop through the API output to generate the information we need for our csv
#for i in range(0,8):
    #    task_id.append(data['docs'][i]['task_id'])
    #    type.append(data['docs'][i]['type'])

####Create a pandas dataframe to output into a csv file
#df = pd.DataFrame(
#    {"task_id": task_id,
     #"type": type
    # }
#)
#print(df)

####Writing our outputs to a csv file
#df.to_csv('output.csv',index=False)
'''' next step is to iterate over the 8 task_ids and create a pandas dataframe
for them with the check i want to implement and output a csv
initial thoughts for output is:
task_id:
type:
label '''

#data_dict = json.loads(data)
#keys = data.keys()
#print(keys)
