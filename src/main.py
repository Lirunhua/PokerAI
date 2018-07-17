#!/usr/bin/env python
from takeAction import TakeAction
import time
import json
from websocket import create_connection
import sys

# pip install websocket-client
AI_name = "GLaDOS"

def doListen():
    try:
        ws = create_connection("ws://poker-dev.wrs.club:3001")
        ws.send(json.dumps({
            "eventName": "__join",
            "data": {
                "playerName": AI_name
            }
        }))
        action = TakeAction()
        while 1:
            result = ws.recv()
            response = action.processRequest(result)
            # for debugging
            print(result)
            sys.stdout.flush()
            
            if response != None:
                ws.send(response)
    except Exception as e:
        print(e)
        doListen()


if __name__ == '__main__':
    doListen()
