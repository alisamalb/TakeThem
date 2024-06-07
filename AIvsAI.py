from takethem.game import Game
from takethem.agents.NNagent import AIagent

import os
import time

def clear_screen():
    # For Windows
    if os.name == 'nt':
        os.system('cls')
    # For Unix-based systems (Linux, macOS)
    else:
        os.system('clear')

game=Game(player1=AIagent,otherplayers=AIagent,automaticRestart=False)
for i in range(5):
    game.players[i+1].training=False
playagain=True
i=0
while playagain:
    print(f"Match number {i//10 +1}")
    game.printPlayersHands()
    game.playerAction()
    clear_screen()
    print(f"Match number {i//10 +1}")
    game.printPlayedCards()
    game.resolveTurn()
    clear_screen()
    playagain=game.checkGameCanContinue()
    i+=1
    
