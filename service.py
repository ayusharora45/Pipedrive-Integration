from flask import Flask, request, json
from dotenv import load_dotenv
import os
import requests

load_dotenv()
API_KEY=os.environ.get("API_KEY")

PIPERDRIVE_PERSON_BASE_URL='https://api.pipedrive.com/v1/persons/'
PIPERDRIVE_PERSON_FIELD_BASE_URL='https://api.pipedrive.com/v1/personFields'

def getPersonInfo(request):
    if request.args.get('id'):
        return getPersonInfoById(request.args.get('id'))
    elif request.args.get('name'):
        return getPersonInfoByName(request.args.get('name'))
    else:
        return 'Enter correct query params'


def getPersonInfoById(id):
    data = requests.get(f"{PIPERDRIVE_PERSON_BASE_URL}{id}?api_token={API_KEY}")
    return json.loads(data.content)


def getPersonInfoByName(name):
    data = requests.get(f"{PIPERDRIVE_PERSON_BASE_URL}find?term={name}&api_token={API_KEY}")
    return json.loads(data.content)

def getCreatedPersonDataAndCustomField(data):
    data['is_new_person']='true'
    data['siq_stop_val_key'] = getCustomFieldInfo(data)
    print('Created person data with custom field value', json.dumps(data))
    return data

def getUpdatedPersonDataAndCustomField(data):
    data['is_new_person']='false'
    data['siq_stop_val_key'] = getCustomFieldInfo(data)
    print('Updated person data with custom field value', json.dumps(data))
    return data

def updatePersonById(id, data):
    data = requests.put(f"{PIPERDRIVE_PERSON_BASE_URL}{id}?api_token={API_KEY}", data)
    return json.loads(data.content)

def getCustomFieldInfo(data):
    allCustomField = requests.get(f"{PIPERDRIVE_PERSON_FIELD_BASE_URL}?api_token={API_KEY}")
    allCustomField = json.loads(allCustomField.content)
    for x in allCustomField['data']:
        if x['name'] == 'SIQ Stop':
            siqStopObj = x
            break
    customFieldId = int(data['current'][siqStopObj['key']])

    for x in siqStopObj['options']:
        if x['id'] == customFieldId:
            return x['label']
    return ''