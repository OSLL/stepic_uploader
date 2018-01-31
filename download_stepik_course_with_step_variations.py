'''
Download a Stepik course
Run with Python 3
'''
USAGE = "USAGE: python download_stepik_course.py <course_ID>"
# imports
import sys
import requests
import json
import os
import datetime

# Enter parameters below:
# Get your keys at https://stepik.org/oauth2/applications/
# (client type = confidential, authorization grant type = client credentials)
client_id = ''
client_secret = ''
api_host = 'https://stepik.org'

# parse args (to get course ID)
if len(sys.argv) != 2:
    print("\nERROR: Incorrect number of arguments")
    print(USAGE)
    exit(-1)
try:
    course_id = int(sys.argv[1])
except:
    print("\nERROR: Course ID was not an integer")
    print(USAGE)
print("Attempting to download course: " + str(course_id))

# Get a token
print("Requesting token...")
auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
response = requests.post('https://stepik.org/oauth2/token/',
                         data={'grant_type': 'client_credentials'},
                         auth=auth)
						 
print("response = " + str(response.json()))			 
if "503" in str(response):
    print("\nERROR: Received 503 error from Stepik")
    print("Perhaps they are doing maintenance? Check Stepik and try again later")
    exit(-1)
token = response.json().get('access_token', None)

if not token:
    print("\nERROR: Unable to authorize with provided credentials")
    print("Client ID:     " + str(client_id))
    print("Client Secret: " + str(client_secret))
    exit(-1)
print("Token requested successfully\n")

# Call API (https://stepik.org/api/docs/) to download a single object
def fetch_object(obj_class, obj_id):
    api_url = '{}/api/{}s/{}'.format(api_host, obj_class, obj_id)
    response = requests.get(api_url,
                            headers={'Authorization': 'Bearer ' + token}).json()
    return response['{}s'.format(obj_class)][0]

# Fetch all objects
def fetch_objects(obj_class, obj_ids):                             # получить список объектов по списку id
    objs = []
    # Fetch objects by 30 items,
    # so we won't bump into HTTP request length limits
    step_size = 30
    for i in range(0, len(obj_ids), step_size):
        obj_ids_slice = obj_ids[i:i + step_size]
        api_url = '{}/api/{}s?{}'.format(api_host, obj_class,
                                         '&'.join('ids[]={}'.format(obj_id)
                                                  for obj_id in obj_ids_slice))
        response = requests.get(api_url,
                                headers={'Authorization': 'Bearer ' + token}
                                ).json()
        objs += response['{}s'.format(obj_class)]
    return objs

# Fetch step source by position with variations
# step sourse: https://stepik.org/api/steps?lesson={}
def fetch_step_objects(lesson_id, position_id):
    objs = []
    api_url = '{}/api/steps?lesson={}'.format(api_host, lesson_id)
    response = requests.get(api_url,
                            headers={'Authorization': 'Bearer ' + token}).json()
    for step in response['steps']:
        if step['position'] == int(position_id):
            step_source = fetch_object('step-source', step['id'])
            objs.append(step_source)
    return objs


# Perform the fetches
course = fetch_object('course', course_id)                   #получить курс
sections = fetch_objects('section', course['sections'])      #получить модули
print("Ready to download course: " + course['title'])

#unit_ids = [unit for section in sections for unit in section['units']]      #получить из модулей id всех уроков
#units = fetch_objects('unit', unit_ids)                                     #по unit_ids получаем все юниты

#lesson_ids = [unit['lesson'] for unit in units]                             #из всех unit получаем список id уроков
#lessons = fetch_objects('lesson', lesson_ids)                               #получить список всех уроков   

#step_ids = [step for lesson in lessons for step in lesson['steps']]         #получить список id всех степов
#steps = fetch_objects('step', step_ids)                                     #получить степы без альтернатив 


for secIndex, section in enumerate(sections):
    print("===== BEGIN SECTION " + str(secIndex+1) + " OF " + str(len(sections)) + " =====")
    unit_ids = section['units']
    units = fetch_objects('unit', unit_ids)

    for unitIndex, unit in enumerate(units): 
        if unitIndex > 0:
            print()
        print("--- Downloading Unit " + str(unitIndex+1) + " of " + str(len(units)) + " ---")
        lesson_id = unit['lesson']
        lesson = fetch_object('lesson', lesson_id)

        qty_steps = len(lesson['steps'])
        for step_position in range(qty_steps):                                       
            print("Downloading step " + str(step_position+1) + " of " + str(qty_steps) + "...")
            step_source = fetch_step_objects(lesson_id, step_position + 1)                                        #получаем все альтернативы степа по номеру урока и по номеру позиции
            for varIndex, step in enumerate(step_source):
                path = [
                    '{} {}'.format(str(course['id']).replace('/','-').zfill(2), course['title'].strip()),
                    '{} {}'.format(str(section['position']).replace('/','-').zfill(2), section['title'].strip()),
                    '{} {}'.format(str(unit['position']).replace('/','-').zfill(2), lesson['title'].strip()),
                    '{}_{}_{}_{}.step'.format(lesson['id'], str(step['position']).zfill(2), step['block']['name'], str(varIndex+1).zfill(2))
                ]
                try:
                    os.makedirs(os.path.join(os.curdir, *path[:-1]))
                except:
                    pass
                filename = os.path.join(os.curdir, *path)
                f = open(filename, 'w')
                data = {
                    'block': step['block'],
                    'id': str(step['id']),
                    'time': datetime.datetime.now().isoformat()
                }
                f.write(json.dumps(data, indent=4, ensure_ascii=False))
                f.close()
                print(filename)
                
    print("===== END SECTION " + str(secIndex+1) + " OF " + str(len(sections)) + " =====\n\n")
