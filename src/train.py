from main import Main
from takeAction import TakeAction
from threading import Thread
import os.path
import random
import time
import sys


class Table:
    def __init__(self, playerCount, names):
        self.playerCount = playerCount
        self.thread = []
        self.players = [Main(n) for n in names]

    def run(self, players):
        for i in range(self.playerCount):
            print(players[i].blackbox.filenameArray)
            self.players[i].action = players[i]
        self.thread = [Thread(target=p.doListen) for p in self.players]
        for t in self.thread:
            t.start()

    def wait(self):
        for t in self.thread:
            t.join()
            sys.stdout.flush()
        for p in self.players:
            p.action.blackbox.saveAll()

def tableConstructor(table):
    def run():
        global lock
        global running
        global botPool
        while running:
            while lock:
                time.sleep(1)
            lock = True
            random.shuffle(botPool)
            temp = [p.action for p in table.players]
            table.run(botPool[:table.playerCount])
            botPool = botPool[table.playerCount:]
            botPool.extend(temp)
            lock = False
            print("now we wait for the game to end")
            table.wait()
            print("The game has ended")
    return Thread(target=run)

# Create the population.
population = 20
everyone = [TakeAction(["../data/trainingFile_%d_1.txt"%i,"../data/trainingFile_%d_2.txt"%i,"../data/trainingFile_%d_3.txt"%i]) for i in range(population)]
botPool = everyone[:] #shallow copy
tables = [tableConstructor(Table(10, ['GLaDOS%d'%i for i in range(10)]))]
lock = False
running = True

for t in tables:
    t.start()

for t in tables:
    t.join()
