# @author: Jess
# uses Deuces library to evaluate our win potential
# win potential depends on how strong our cards are now, and how strong they are likely to be in the future.
# ex: almost having a full house might be worth staying in the game

# Need to handle:
# handling strong or weak holeCards at start
# card potential
# current score from evaluator
# how much to bet depending on card strength
# when to stay in the game if bet is high and we don't have many chips

from deuces import Card
from deuces import Evaluator

board = [
    Card.new('As'),
    Card.new('Ks'),
    Card.new('Js')
]
hand = [
    Card.new('Qd'),
    Card.new('Td')
]

evaluator = Evaluator()

Card.print_pretty_cards(board + hand)
p1_score = evaluator.evaluate(board, hand)
p1_class = evaluator.get_rank_class(p1_score)
print("Player 1 hand rank = %d (%s)\n" % (p1_score, evaluator.class_to_string(p1_class)))

class decisionMaker9000:
    evaluator = Evaluator() # evaluates 1 (best) to 7462 (worst)

    def __init__(self, table, players, action):
        self.table = table
        self.players = players
        self.boardCards = table["board"]
        # self.holeCards = 
        self.action = action

    # evaluate our cards right now
    def evaluateHand(self):
        return evaluator.evaluate(boardCards, holeCards)
