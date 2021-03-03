import os
import requests

def searchProperties():
    url = "https://realtor.p.rapidapi.com/properties/v2/list-for-sale"
    querystring = {"city":"hartford","limit":"5","offset":"0","state_code":"CT","sort":"relevance"}
    headers = {
        'x-rapidapi-key': "f11e08f9bemshea6d5c2ec70540fp1b926djsn841f40eb598e",
        'x-rapidapi-host': "realtor.p.rapidapi.com"
        }
    response = requests.request("GET", url, headers=headers, params=querystring)
    properties = response.json()
    properties_list = []
    for i in range (len(properties['properties'])):
        properties_list.append(properties['properties'][i])
    return properties_list