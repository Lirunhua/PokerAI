# from slackclient import SlackClient
import json
import requests
import config

def sendMessage(message):
    slack_data = {'text': message}

    response = requests.post(
        config.webhook_url, data=json.dumps(slack_data),
        headers={'Content-Type': 'application/json'}
    )
    if response.status_code != 200:
        raise ValueError(
            'Request to slack returned an error %s, the response is:\n%s'
            % (response.status_code, response.text)
    )