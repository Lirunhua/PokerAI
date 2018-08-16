# Team Intern PokerAI

### TODO list:
- [x] Compare hand to dataset and create meaningful data from it.
- [x] Transform data into an input vector.
- [x] Transform our output vector in a json object as a response for the server.
- [x] Create a training algorithm
- [x] Save internal state and load it every time.
- [x] Optimise calculation time to under 1 seconds and time out after 5.
- [x] Train our bot.
- [x] Win!

As a team of interns working at Trend Micro on summer contract, we decided to compete in their Poker AI Challenge. Unsupervised machine learning was implemented so that our AI, GLaDOS, could gradually improve the more games it plays. A genetic algorithm was used in training so GLaDOS can play a game of poker against many versions of itself, and the dataset of the winner would be kept and re-cloned for future rounds. GLaDOS successfully learned when to call, check, bet, raise, fold, and all in!
