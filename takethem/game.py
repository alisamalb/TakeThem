from .deck import Deck
from .agents.cliPlayer import cliPlayer
from .agents.RandomAgent import RandomAgent

class Game:
    def __init__(self,n_players=6,automaticRestart=False):
        """Initializes a game, based on the number of players.
        The spot of the first player is by default assigned to the user.
        
        Args:
            n_players (int, optional): The number of players. Defaults to 6.
            automaticRestart(bool,optional): Ask for a prompt before starting new game.
        """
        self.automaticRestart=automaticRestart
        self.deck=Deck(n_players*10+4)
        
        #Create the players and assign them to this game
        self.players=[cliPlayer(self)]
        [self.players.append(RandomAgent(self)) for i in range(n_players-1)]
        
        self.newGame()
    
    def newGame(self):    
        #Create empty table
        self.tableRows=[[],[],[],[]]
        self.playedCards=[]
        self.removedCards=[]
        
        #Distribute cards
        self._dealCards()
        self._prepareTableRows()

    def _dealCards(self):
        "Draws and distributes 10 cards for each player."
        for player in self.players:
            player.draw(10)
    
    def _prepareTableRows(self):
        """Draws for cards from the deck and places them
        at the beginning of each tableRow.
        """
        for i in range(4):
           self.tableRows[i]=[self.deck.draw_card()] 
    
    def playerAction(self):
        """Makes every player play a card."""
        
        for player in self.players:
            self.playedCards.append(player.playCard())
    
    
    def resolveTurn(self):
        self.playedCards.sort(key=lambda x: x.n)
        for card in self.playedCards:
            checkIfSmall=True
            for row in self.tableRows:
                if card.n>row[-1].n:
                    checkIfSmall=False
                    
            if checkIfSmall:
                self._resolveSmallNumberCard(card)
            
            else:
                rowTarget=0
                rowDifference=1000
                
                for i,row in enumerate(self.tableRows):
                    difference=card.n-row[-1].n
                    if difference>0 and difference<rowDifference:
                        rowTarget=i
                        rowDifference=difference
                
                if len(self.tableRows[rowTarget])<5:
                    self.tableRows[rowTarget].append(card)   
                else:
                    cardOwner=card.lastOwner
                    cardOwner.takePenalty(rowTarget,card)

        self.playedCards=[]    

    def _resolveSmallNumberCard(self,card):
        cardOwner=card.lastOwner
        cardOwner.resolveSmallNumberCard(card)
    
    def printRows(self):
        """Prints table rows.
        """
        print("--Table Rows--")
        for row in self.tableRows:
            row_string=""
            for card in row:
                row_string+=(f"{card.n} (+{card.penalty})".rjust(10," "))
            print(row_string)
            
    def printScoreboard(self):
        print("--Scoreboard--")
        for i,player in enumerate(self.players):
            print(f"Player {i+1}: {player.penalties} pt.")
            
    def printPlayersHands(self,full=False):
        """Displays scoreboard, table rows and players' hands.
        By default, only Player 1's hand is shown.

        Args:
            full (bool, optional): Display all players' hand. Defaults to False.
        """
       
        self.printScoreboard()
        self.printRows()

        if full:
            for i,player in enumerate(self.players):
                print(f"--Player {i+1}'s hand--")
                hand_string=""
                for card in player.hand:
                    hand_string+=(f"{card.n} (+{card.penalty})".rjust(10," "))
                print(hand_string)
        
        else:
            print("--Player 1 hand--")
            player_hand_string=""
            for i,card in enumerate(self.players[0].hand):
                player_hand_string+=(f"{i+1}. {card.n} (+{card.penalty})\n")
            print(player_hand_string)
    
    def printPlayedCards(self):
        """Displays scoreboard, table rows and played cards.
        """
        self.playedCards.sort(key=lambda x: x.n)
        self.printScoreboard()
        self.printRows()
        print("--Played cards--")
        row_string=""
        for card in self.playedCards:
                row_string+=(f"{card.n} (+{card.penalty})".rjust(10," "))
        print(row_string)

    def checkGameEnded(self):
        cardsToPlay=sum([len(player.hand) for player in self.players])
        if cardsToPlay==0:
            if self.automaticRestart:
                self.newGame()
            else:
                response='42'
                while response not in ["yes","no"]:
                    response=input("Do you want to play again? [yes/no]\n")
                
                if response=="yes":
                    self.newGame()
                else:
                    quit()
