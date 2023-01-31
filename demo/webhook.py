import requests
import json

webhook_url = "https://webhook.site/1337f482-8dd6-430d-83b4-c8a2ccf91438"

data = {
    'name': 'DevOps Journey',
    'Channel URL': 'https://www.youtube.com/channel/UC4Snw5yrSDMXys31118U3gg'
    }

r = requests.post(webhook_url, data=json.dumps(data), headers={'content-Type': 'application/json'})

print(r.text)
