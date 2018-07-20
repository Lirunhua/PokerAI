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

    def doListen(self):
        try:
            ws = create_connection("ws://poker-dev.wrs.club:3001")
            ws.settimeout(5000)
            ws.send(json.dumps({
                "eventName": "__join",
                "data": {
                    "playerName": self.AI_name
                }
            }))
            action = TakeAction(self.filenames)
            loop = True
            while loop:
                result = ws.recv()
                response = action.processRequest(result)
                # for debugging
                print(result)
                sys.stdout.flush()
                
                if response != None:
                    ws.send(response)
                loop = False
        except Exception as e:
            print(e)
            #self.doListen()


if __name__ == '__main__':
    m = Main()
    m.doListen()
