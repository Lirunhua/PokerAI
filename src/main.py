#!/usr/bin/env python
from takeAction import TakeAction
import time
import json
from websocket import create_connection
import sys

class Main:
    def __init__(self, name="197818", filenames = ["../data/file1.txt","../data/file2.txt","../data/file3.txt"]):
        self.AI_name = name
        self.filenames = filenames
        self.debugMode = False

    # default url is test server.
    def doListen(self, url="ws://canada-ai-warmup-fbd9b486707f3df1.elb.us-east-1.amazonaws.com/"):
        try:
            ws = create_connection(url)
            ws.settimeout(5000)
            ws.send(json.dumps({
                "eventName": "__join",
                "data": {
                    "playerName": self.AI_name
                }
            }))
            action = TakeAction(self.filenames, self.debugMode)
            loop = True
            while loop:
                result = ws.recv()
                response = action.processRequest(result) if result != "" else None
                sys.stdout.flush()
                
                if response != None:
                    ws.send(response)
                    #loop = False
        except Exception as e:
            print("An error has occured")
            print(e)
            sys.stdout.flush()
            self.doListen()


if __name__ == '__main__':
    m1 = Main()
    m1.doListen("ws://canada-ai-warmup-battle-7da4ce4b0426974c.elb.us-east-1.amazonaws.com/")
