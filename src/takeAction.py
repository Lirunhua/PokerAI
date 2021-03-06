import json
import random
from blackbox import BlackBox
import slackClient


class TakeAction:
    def __init__(self, files, debugMode):
        self.__cards = None
        self.__tableCards = None
        self.__table = None
        self.__players = None
        self.doCallback = False
        self.endGameCallback = None
        self.win = True
        self.debugMode = debugMode
        self.slackMessage = ""
        self.blackbox = BlackBox(files, 6, 7, 7, 6)
        self.playerName = -1
        self.response = [0, 0, 0, 0, 0, 0]
        self.reload = 0
        self.betAmount = 100

    def setCallback(self, callback):
        self.doCallback = True
        self.endGameCallback = callback

    def getVectorResponse(self):
        # format of response vector: [call/check, fold, allin, raise/bet, reload (T/F), bet amount]
        # we can also perform a check (i.e. calling with an amount of 0 chips)
        cards = self.__cards.copy()
        cards.extend(self.__tableCards)
        self.response = self.blackbox.run(cards, self.__players, self.__table)
        if not self.debugMode:
            print(str(self.response))


    # Parses the Json and chooses an appropriate action
    def processRequest(self, jsonObject):
        # if the json is form a file use json.load(file)
        try:
            action = json.loads(jsonObject)
        except Exception as e:
            return None

        if "eventName" not in action:
            print("json object has no eventName")
            print(str(action))
            return None

        self.slackMessage = ""  # reset message
        if not self.debugMode:
            print(str(action["eventName"]))

        # The Json for players and table is different for __action, __bet and __show_action.
        if action["eventName"] == "__action":
            if self.playerName == -1:
                self.playerName = action["data"]["self"]["playerName"]
                if not self.debugMode:
                    print("Hello. My name is " + str(self.playerName))

            self.getVectorResponse()
            response = self.response[:4]

            # It's our turn, we should respond with an __action.
            actionObj = {
                "eventName": "__action",
                "data": {
                    "action": ""
                }
            }
            maxValue = max(response)
            maxIndex = response.index(maxValue)

            if maxIndex == 0:
                actionObj["data"]["action"] = "call"
            elif maxIndex == 1:
                actionObj["data"]["action"] = "fold"
            elif maxIndex == 2:
                actionObj["data"]["action"] = "allin"
                if action["data"]["self"]["chips"] >= 5000:
                    self.slackMessage = "Oh no. We are betting " + str(action["data"]["self"]["chips"]) + " chips!!! Wish me luck."
                    self.__sendSlackStatus()
            elif maxIndex == 3:
                actionObj["data"]["action"] = "raise"

            self.playerName = action["data"]["self"]["playerName"]

            return json.dumps(actionObj)
        elif action["eventName"] == "__show_action":
            # Broadcast to everyone when someone makes an __action (on their turn)
            self.__setTable(action["data"]["table"])
            self.__setPlayers(action["data"]["players"])
        elif action["eventName"] == "__bet":
            # possibilities: [check, bet, fold]
            if not self.debugMode:
                print("We are betting!\n")
            self.getVectorResponse()
            response = self.response[:2]    # index 2 is "allin" which is not applicable here
            response.append(self.response[3])

            actionObj = {
                "eventName": "__action",
                "data": {
                    "action": "",
                    "amount": 0
                }
            }
            maxValue = max(response)
            maxIndex = response.index(maxValue)
            self.betAmount = self.response[5]

            if maxIndex == 0:
                actionObj["data"]["action"] = "check"
            elif maxIndex == 1:
                actionObj["data"]["action"] = "fold"
            elif maxIndex == 2:
                actionObj["data"]["action"] = "bet"
                actionObj["data"]["amount"] = int(self.betAmount * action["data"]["self"]["chips"])

            return json.dumps(actionObj)

        elif action["eventName"] == "__deal":
            # The small and big blinds are set!
            self.__setTable(action["data"]["table"])
            self.__setPlayers(action["data"]["players"])
        elif action["eventName"] == "__start_reload":
            # we should either reload or not, so T/F
            if not self.debugMode:
                print("Reload probability " + str(self.response[5]) + "\n")
            if self.response[5] > 0.5:
                if not self.debugMode:
                    print("Reloaded!\n")
                return json.dumps({"eventName": "__reload"})
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
            self.win = self.__Survive(action)
            if self.win:
                self.slackMessage = "We survived!"
            else:
                self.slackMessage = "We didn't survive."
            self.__sendSlackStatus()

            if self.doCallback:
                self.endGameCallback(self)

        elif action["eventName"] == "__new_peer":
            # response to our __join request
            if not self.debugMode:
                print("I'm in!")

        return None

    # Checks if we survived or not.
    def __Survive(self, action):
        for element in action["data"]["players"]:
            if not self.debugMode:
                print(str(element))
            if element["playerName"] == self.playerName and element["isSurvive"]:
                return True
        return False
    #     self.__sendSlackStatus()

    # sends AI status to slack webhook
    def __sendSlackStatus(self):
        if not self.debugMode :
            slackClient.sendMessage(self.slackMessage)


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
