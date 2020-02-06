import os
import sys
import json
import requests
import urllib3

#Disable the insecure request warning for the infoblox server.
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

infoToken = os.environ['infobloxtoken']

ADDRESS = 'https://infoblox.XXXXX.XXX'
VERSION = '2.10'
PATH = '/wapi/v' + VERSION + '/'
DEFAULT_OBJECT_TYPE = 'network'
JSON = 'application/json'
URLENCODED = 'application/x-www-form-urlencoded'
DEFAULT_CONTENT_TYPE = URLENCODED

def perform_request(operation, ref='', params='', payload='', \
                    object_type=DEFAULT_OBJECT_TYPE, \
                    content_type=DEFAULT_CONTENT_TYPE):
    #print("object_type2: "+DEFAULT_OBJECT_TYPE)
    auth_header = 'Basic %s' % (infoToken)
    headers = {'Authorization':auth_header, 'Content-Type': content_type}
    if ref:
        url = ADDRESS + PATH + ref
    else:
        url = ADDRESS + PATH + object_type
    if params:
        url += params
    print("operation: "+operation)
    print("url: "+url)
    print("headers: "+str(headers))
    print("data: "+str(payload))
    try:
        if payload:
            print("running Payload...")
            response = requests.request(operation, url, headers=headers, data=json.dumps(payload), verify=False) 
            return response
        else:
            print("no Payload...")
            response = requests.request(operation, url, headers=headers, verify=False) 
            return response
    except Exception as e:    
        print("perform_request Failed! Exception: "+e.error)


def GetRecord(ref, params):
    #Read this network with extensible attributes and comment return fields
    response = perform_request('GET', ref, params)
    print("response: "+str(response.text))
    print("*************************")

def CreateCRecord(objecttype, payload):   #ref, params, payload):
    #Create Canonical Name w/extensible attributes and comment return fields
    response = perform_request('POST', payload=payload, object_type=objecttype, content_type=JSON)
    print("response: "+str(response.text))
    print("*************************")

def DisableRecord(reference_id, boolstate):
    #To Disable a CNAME, the disabledata variable holds the required payload.
    if boolstate:
        payload = {"disable":True}
    else:
        payload = {"disable":False}
    response = perform_request('PUT', ref=reference_id, payload=payload, content_type=JSON)
    print("response: "+str(response.text))
    print("*************************")

def DeleteRecord(reference_id):
    response = perform_request('DELETE', ref=reference_id, object_type='record:cname')
    print("response: "+str(response.text))
    print("*************************")


def main():
    #Main function: run network and host examples.
    #GetRecord('record:cname?name~=hub.XXXXX.XXX','&_return_fields=name,disable,canonical,extattrs,view,zone')
    #GetRecord('record:a?name~=www.XXXXXX.XXX','&_return_fields=name,disable,extattrs')
    #GetRecord('record:a?name~=website.XXXXX.XXX','&_return_fields=name,comment,disable,extattrs,view,zone')
    
    #CreateCRecord('record:cname', {'canonical': 'website.XXXXXX.com.cdn.XXXXXXX.net', 'name': 'website.XXXXXX.com', 'view': 'default.External'})

    #DisableRecord('',False)
    #DeleteRecord('record:cname/XXXXXXXXXXXXXXZZZZZZZZZQQQQQQQQQQQQQQQQQ:website.XXXXXXX.com/default.External')
    


if __name__ == '__main__':
    sys.exit(main())
