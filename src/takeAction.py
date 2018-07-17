import json

class TakeAction:
    def __init__(self):
        self.__table = None
        self.__players = None

    # Parses the Json and chooses an appropriate action
    def processRequest(self, jsonObject):
        # if the json is form a file use json.load(file)
        action = json.loads(jsonObject)

        # The Json for players and table is diffrent for __action, __bet and __show_action.
        if action["eventName"] == "__action":
            # It's our turn, we should respond with an __action.
            return json.dumps({
                "eventName": "__action",
                "data": {
                    "action": "call",
                    "playerName": "player1"
                }
            })
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
                    "playerNam  e": "player1",
                    "amount": 100
                }
            })
        elif action["eventName"] == "__deal":
            # The small and big blinds are set!
            self.__setTable(action["data"]["table"])
            self.__setPlayers(action["data"]["players"])
        elif action["eventName"] == "__start_reload":
            # We got 3 seconds to reload our chips. (automatic action if we have no chips left) The max count limit is set before the match
            self.__setPlayers(action["data"]["players"])
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
    #   board"          String Array    Probably the cards in the middle.
    #   roundCount      int             Max amount of reloads I think.
    #   raiseCount      int             Not sure.
    #   betCount        int             Number of raises this round.
    #   totalBet        int             I think this is the pot.
    #   smallBlind      object          Name of the player and amount.
    #   bigBlind        object          Name of the player and amount.
    #
   ##
    def __setTable(self, table):
        self.__table = table

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
        self.__players = players
