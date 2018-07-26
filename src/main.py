#!/usr/bin/env python
from takeAction import TakeAction
import json
from websocket import create_connection
import sys

class Main:
    def __init__(self, name="197818", filenames = ["../data/file1.txt","../data/file2.txt","../data/file3.txt"]):
        self.AI_name = name
        self.filenames = filenames
        self.action = TakeAction(self.filenames)

    # default url is test server.
    def doListen(self, url="ws://poker-dev.wrs.club:3001"):
        try:
            ws = create_connection(url)
            ws.settimeout(5000)
            ws.send(json.dumps({
                "eventName": "__join",
                "data": {
                    "playerName": self.AI_name
                }
            }))
            loop = True
            while loop:
                result = ws.recv()
                response = self.action.processRequest(result) if result != "" else None
                sys.stdout.flush()
                
                if response == False:
                    loop = False
                elif response != None:
                    ws.send(response)
            print ("exited the loop!")
        except Exception as e:
            print("An error has occured")
            print(e)
            sys.stdout.flush()
            self.doListen()


if __name__ == '__main__':
    m1 = Main()
    m1.doListen("ws://canada-ai-warmup-battle-7da4ce4b0426974c.elb.us-east-1.amazonaws.com/")
