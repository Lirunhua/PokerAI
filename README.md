# Team Intern PokerAI
Team: David Bonsant, Jess cannarozzo, Dharina Hanumunthadu, Rouzbeh Majidi, Dieter Verhufen

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

Since all poker games lasted diffrent lenghts of time, we didn't use generations to train our bot. Instead we had a pool of 10 bots waiting for a game to end (games range from 3 to 10 players). When a N player game ended, N players were chosen from the bot pool to play the next game. The winners from the game that just finished would be put back in to the bot pool and the losers would be discarded to be repalced by a mix of 2 winning bots. The new bot would then be randomly mutated and then inserted back into the bot pool.
