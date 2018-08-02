#!/usr/bin/env python
import os
from takeAction import TakeAction
import json
from websocket import create_connection
import sys, os

class Main:
    def __init__(self, name="197818", debug = False, filenames = ["../data/file1.txt","../data/file2.txt","../data/file3.txt"]):
        self.AI_name = name
        self.filenames = filenames
        self.debugMode = debug
        self.action = TakeAction(self.filenames, self.debugMode)
        

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
            loop = True
            while loop:
                result = ws.recv()
                response = self.action.processRequest(result) if result != "" else None
                sys.stdout.flush()

                if response is not None:
                    if not self.debugMode:
                        print(response)
                    ws.send(response)
            print ("exited the loop!")
        except Exception as e:
            print("An error has occured")
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            sys.stdout.flush()
            self.doListen()

    def setAction(self, action):
        self.action = action


if __name__ == '__main__':
    m1 = Main()
    m1.doListen("ws://canada-ai-warmup-battle-7da4ce4b0426974c.elb.us-east-1.amazonaws.com/")
