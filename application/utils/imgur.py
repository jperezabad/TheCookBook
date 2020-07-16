import requests
import json
from flask import current_app

def uploadImage(image : str):
    url = 'https://api.imgur.com/3/image'
    clientId = current_app.config['IMGUR_CLIENT_ID']
    payload = {'image': image}
    headers = { 'Authorization': 'Client-ID ' + clientId }
    response = requests.request('POST', url, headers = headers, data = payload)
    json = response.json()
    if response.status_code != 200:
        return None
    link = json['data']['link']
    return link

def uploadBase64(image):
    url = 'https://api.imgur.com/3/image'
    clientId = current_app.config['IMGUR_CLIENT_ID']
    # Fixing base64 encoding after HTTP request
    fixedImage = image.replace(' ', '+')
    payload = {'image': fixedImage}
    headers = { 'Authorization': 'Client-ID ' + clientId }
    response = requests.request('POST', url, headers = headers, data = payload)
    json = response.json()
    if response.status_code != 200:
        return None
    link = json['data']['link']
    return link