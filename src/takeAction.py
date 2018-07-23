import json
import random
from blackbox import BlackBox


class TakeAction:
    def __init__(self, files):
        self.__cards = None
        self.__tableCards = None
        self.__table = None
        self.__players = None
        self.blackbox = BlackBox(files, 6, 7, 7, 5)

    def getVectorResponse(self):
        # format of vector: [check, fold, allin, raise, bet]
        response = [random.random(), random.random(), random.random(), random.random(), random.random()]
        print("The response vector is: ", response, "\n")
        return response


    # Parses the Json and chooses an appropriate action
    def processRequest(self, jsonObject):
        # if the json is form a file use json.load(file)
        action = json.loads(jsonObject)
        print(action["eventName"])

        # The Json for players and table is diffrent for __action, __bet and __show_action.
        if action["eventName"] == "__action":
            cards = self.__cards.copy()
            cards.extend(self.__tableCards)
            response = self.blackbox.run(cards, self.__players,self.__table)
            print(response)
            # It's our turn, we should respond with an __action.
            actionObj = {
                "eventName": "__action",
                "data": {
                    "action:": None
                }
            }
            maxValue = max(response)
            maxIndex = response.index(maxValue)

            if maxIndex == 0:
                actionObj["data"]["action"] = "check"
            elif maxIndex == 1:
                actionObj["data"]["action"] = "fold"
            elif maxIndex == 2:
                actionObj["data"]["action"] = "allin"
            elif maxIndex == 3:
                actionObj["data"]["action"] = "raise"
            elif maxIndex == 4:
                actionObj["data"]["action"] = "call"

            return json.dumps(actionObj)
        elif action["eventName"] == "__show_action":
            # Brodcasted to everyone when someone makes an __action (on their turn)
            self.__setTable(action["data"]["table"])
            self.__setPlayers(action["data"]["players"])
        elif action["eventName"] == "__bet":
            # it's out turn, we should do a bet __action but I'm not exactly sure of when it's called.
            return json.dumps({
                "eventName": "__action",
                "data": {
                    "action": "bet",
                    "amount": 100
                }
            })
        elif action["eventName"] == "__deal":
            # The small and big blinds are set!
            self.__setTable(action["data"]["table"])
            self.__setPlayers(action["data"]["players"])
        elif action["eventName"] == "__start_reload":
            # We got 3 seconds to reload our chips.
            #self.__setPlayers(action["data"]["players"])
            return json.dumps({"eventName" : "__reload"})
        elif action["eventName"] == "__new_round":
            # The round begins, we have some useful info here.
            self.__setTable(action["data"]["table"])
            self.__setPlayers(action["data"]["players"])
        elif action["eventName"] == "__round_end":
            # End of a round, shows everything. Usefull for dynamic learning
            self.__setTable(action["data"]["table"])
            self.__setPlayers(action["data"]["players"])
        elif action["eventName"] == "__game_over":
            # Shows the winner
            print("The cake was a lie!")
        elif action["eventName"] == "__new_peer":
            # response to our __join request
            print("I'm in!")

        return None
    
    ##
    #
    # Table object
    #
    #   tableNumber     int             Id of the table.
    #   roundName       String          Name of the round. (preflop, flop, turn, river)
    #   board           String Array    Probably the cards in the middle.
    #   roundCount      int             Max amount of reloads I think.
    #   raiseCount      int             Not sure.
    #   betCount        int             Number of raises this round.
    #   totalBet        int             I think this is the pot.
    #   smallBlind      object          Name of the player and amount.
    #   bigBlind        object          Name of the player and amount.
    #
   ##
    def __setTable(self, table):
        tbl = []
        tbl.append(self.normalize(table['tableNumber']))
        tbl.append(self.normalize(table['roundCount']))
        tbl.append(self.normalize(table['raiseCount']))
        tbl.append(self.normalize(table['betCount']))
        tbl.append(self.normalize(table['totalBet']))
        tbl.append(self.normalize(table['smallBlind']['amount']))
        tbl.append(self.normalize(table['bigBlind']['amount']))
        self.__tableCards = [self.__parseCards(c) for c in table['board']]
        self.__table = tbl


    ##
    #
    # Players should be ab array of player objects.
    #
    # Player object:
    #   playerName      String          Name of the player.
    #   chips           int             Amount of money available.
    #   folded          boolean         Has the player folded yet.
    #   allIn           boolean         Is the player All in.
    #   cards           String Array    The player's cards.
    #   isSurvive       boolean         Not sure.
    #   reloadCount     int             How many times the player has reloaded.
    #   roundBet        int             Not sure, probably the big blind or something.
    #   bet             int             What the player has bet already I think.
    #
   ##
    def __setPlayers(self, players):
        plrs = []
        for plr in players:
            arr = []
            arr.append(self.normalize(plr["chips"]))
            arr.append(self.normalize(plr["reloadCount"]))
            arr.append(self.normalize(plr["roundBet"]))
            arr.append(self.normalize(plr["bet"]))
            arr.append(int(plr["folded"]))
            arr.append(int(plr["allIn"]))
            arr.append(int(plr["isSurvive"]))
            plrs.append(arr)
            if 'cards' in plr:
                self.__cards = [self.__parseCards(c) for c in plr['cards']]
        self.__players = plrs

    def normalize(self, x):
        return 0 if x == 0 else 1/float(x)

    def __parseCards(self, card):
        c = []
        num = "A23456789TJQK".index(card[0]) * 4 + "HDCS".index(card[1])
        for i in [32,16,8,4,2,1]:
            c.append(1 if num >= i else 0)
            num = num - i if num >= i else num
        return c
