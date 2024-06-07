from takethem.game import Game
from takethem.agents.RandomAgent import RandomAgent
from takethem.agents.NNagent import AIagent
from takethem.agents.MinimumLogicAgent import MinimumLogicAgent
import random
import os
import time
import matplotlib.pyplot as plt
import numpy as np

def clear_screen():
    # For Windows
    if os.name == 'nt':
        os.system('cls')
    # For Unix-based systems (Linux, macOS)
    else:
        os.system('clear')

def playMatch(classes):
    game=Game(playerClasses=classes,automaticRestart=False)
    i=0
    while i<10:
        game.printPlayersHands()
        game.playerAction()
        clear_screen()
        print(f"Match number {i//10 +1}")
        game.printPlayedCards()
        game.resolveTurn()
        clear_screen()
        if i==9:
            return [p.penalties for p in game.players]
        playagain=game.checkGameCanContinue()
        i+=1


aiscores=[]
randomscores=[]
minlogicscores=[]
scoreslist=[aiscores,randomscores,minlogicscores]
classes=[AIagent,RandomAgent,MinimumLogicAgent]



for j in range(100):
    playerclass=[random.randrange(0,3) for x in range(6)]
    players=[classes[x] for x in playerclass]
    scores=playMatch(players)
    for i in range(6):
        scoreslist[playerclass[i]].append(scores[i])
    print([np.mean(x) for x in scoreslist])
    time.sleep(1)

plotrange=(0,40)
ai_hist=np.histogram(aiscores,range=plotrange,bins=30)
rand_hist=np.histogram(randomscores,range=plotrange,bins=30)
min_hist=np.histogram(minlogicscores,range=plotrange,bins=30)
plt.plot(ai_hist[0])
plt.plot(rand_hist[0])
plt.plot(min_hist[0])
plt.show()