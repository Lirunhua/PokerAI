from main import Main
from takeAction import TakeAction
from threading import Thread
import os.path
import random
import time
import sys


class Table:
    def __init__(self, playerCount, names, players):
        self.playerCount = playerCount
        self.thread = []
        self.players = [Main(n, True) for n in names]
        self.playerEndCount = 0
        self.winners = []
        # remove default network
        for i in range(self.playerCount):
            self.players[i].setAction(players[i])
        # run players forever
        for p in self.players:
            Thread(target=p.doListen).start()

    # Builds a table thread that manages players in a table
    def tableConstructor(self):
        def threadRun():
            global lock
            global running
            global botPool
            while running:
                while lock:
                    time.sleep(1)
                lock = True
                random.shuffle(botPool)
                temp = [p.action for p in self.players]
                self.run(botPool[:self.playerCount])
                botPool = botPool[self.playerCount:]
                botPool.extend(temp)
                lock = False
                print("now we wait for the game to end")
                self.wait()
                print("The game has ended")
        return Thread(target=threadRun)

    def run(self, players):
        # Assign network to players.
        for i in range(self.playerCount):
            #print(players[i].blackbox.filenameArray)
            self.players[i].setAction(players[i])
            # assign callback
            self.players[i].action.setCallback(self.end)
    
    # Callback for end of game.
    def end(self, player):
        if player.win:
            self.winners.append(player.blackbox)
        self.playerEndCount += 1

    def wait(self):
        loop = True
        while loop:
            loop = self.playerEndCount < self.playerCount
        sys.stdout.flush()
        # copy and mutate winners
        for p in self.players:
            if not p.action.win:
                p.action.blackbox.clone(random.choice(self.winners))
                p.action.blackbox.cross(random.choice(self.winners))
            p.action.blackbox.saveAll()
        self.playerEndCount = 0




# Create the population.
population = 25
everyone = [TakeAction(["../data/trainingFile_%d_1.txt"%i,"../data/trainingFile_%d_2.txt"%i,"../data/trainingFile_%d_3.txt"%i], True) for i in range(population)]
botPool = everyone[:] #shallow copy
tables = [
    Table(10, ['GLaDOS%d'%i for i in range(10)], botPool[:10]).tableConstructor(),
    Table(4, ['GLaDOS1%d'%i for i in range(4)], botPool[10:14]).tableConstructor()
]
botPool = botPool[14:]
lock = False
running = True

print("Starting table thread!")
for t in tables:
    t.start()

for t in tables:
    t.join()
