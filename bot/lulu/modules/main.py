import os
from dotenv import load_dotenv

load_dotenv('../.env')

bot_token = os.getenv('DISCORD_TOKEN')
app_id = os.getenv('LULU_APP_ID')

import requests

print(app_id, bot_token)
url = f"https://discord.com/api/v9/applications/{app_id}/commands"

# This is an example CHAT_INPUT or Slash Command, with a type of 1
json = {
    "name": "schedule",
    "type": 1,
    "description": "Send upcomming pro matches",
    "options": [
        {
            "name": "region",
            "description": "Region",
            "type": 3,
            "required": True,
            "choices": [
                {
                    "name": "ALL",
                    "value": "global"
                },
                {
                    "name": "VCS",
                    "value": "VCS"
                },
                {
                    "name": "LPL",
                    "value": "LPL"
                },
                {
                    "name": "LCK",
                    "value": "LCK"
                },
                {
                    "name": "LCS",
                    "value": "LCS"
                },
                {
                    "name": "LEC",
                    "value": "LEC"
                }
            ]
        },
        {
            "name": "image",
            "description": "Send image instead of text",
            "type": 5,
            "required": False
        }
    ]
}

# For authorization, you can use either your bot token
headers = {
    "Authorization": f"Bot {bot_token}"
}

#r = requests.post(url, headers=headers, json=json)
r = requests.patch(url + '/941631465035288618', headers=headers, json=json)
print(r.status_code)
print(r.content.decode())