from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from discord_interactions import verify_key
from dotenv import load_dotenv
import os
import requests
from .modules import loldata
# Create your views here.

@csrf_exempt
def index(request):
    load_dotenv()
    verified = verify_key(request.body, request.META['HTTP_X_SIGNATURE_ED25519'], request.META['HTTP_X_SIGNATURE_TIMESTAMP'], os.getenv('CLIENT_PUBLIC_KEY'))
    if not verified:
        return HttpResponse(status=401)

    body = json.loads(request.body)
    print(body)
    if body['type'] == 1:
        res = {
            'type': 1
        }
        return HttpResponse(json.dumps(res))
    lol = loldata.LOLData()
    if body['type'] == 2:
        data = body['data']
        res = {

        }
        if data['name'] == 'schedule':
            options = data['options']
            regions = []
            image = False
            for option in options:
                if option['name'] == 'region':
                    regions.append(option['value'])
                if option['name'] == 'image':
                    image = option['value']
            res = {
                'type': 4,
                'data': {
                    'tts': False,
                    'content': lol.filtered_matches(to_string=True, regions=regions),
                    'embeds': [],
                    'allowed_mentions': {
                        'parse': []
                    }
                }
            }
        
        url = f'https://discord.com/api/v9/interactions/{body["id"]}/{body["token"]}/callback'
        bot_token = os.getenv('DISCORD_TOKEN')
        r = requests.post(url, json=res)
        print(url, r.status_code)
        return HttpResponse(status=200)
    return HttpResponse(status=404)