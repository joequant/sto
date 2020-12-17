#!/usr/bin/python3

import requests
import json
import os

script_dir = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(script_dir, 'config.json')) as f:
    config = json.load(f)

    #resp = requests.get('https://todolist.example.com/tasks/')
#if resp.status_code != 200:
#    # This means something went wrong.
#    raise ApiError('GET /tasks/ {}'.format(resp.status_code))
#for todo_item in resp.json():
#    print('{} {}'.format(todo_item['id'], todo_item['summary']))
