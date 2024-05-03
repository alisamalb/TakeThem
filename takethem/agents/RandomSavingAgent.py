import random
"""This class defines a random agent for the game. This type of player
chooses a random card from their own hand. If the card has a small number,
it chooses a random row to take penalties from. Once the game has finished,
the agent asks for a new match."""

class RandomSavingAgent:
    def __init__(self,game, save_every=20,play_n_games=1000, file_output='output.txt', overwrite=True):
        """Initializes a random agent for the game.

        Args:
            game: An instance of the game environment.
        """
        self.game=game
        self.hand=[]
        self.penalties=0
        
        self.file_output=file_output
        if overwrite:
            self.overwriteFile()
        self.play_n_games=play_n_games
        self.n_games_performed=0
        self.save_every=save_every
        self.latest_game_staus=[]
        self.latest_played_card=None
        self.previous_penalties=0
        self.status=""
        
    def draw(self,n=1):
        """Draws cards from the deck of the game.

        Args:
            n (int, optional): Number of cards to draw. Defaults to 1.
        """
        if n==1:
            self.hand.append(self.game.deck.draw_card())
        else:
            self.hand+=self.game.deck.draw_cards(n)
        
        self.hand.sort(key=lambda x: x.n)
        for card in self.hand:
            card.setOwner(self)
    
    def playCard(self):
        """Mimics player's turn by playing a random card from the hand."""
        
        if self.latest_played_card: #From the 2nd turn on, run this cycle
            self.status+=","+str(self.latest_played_card.n)
            self.status+=","+str(self.penalties-self.previous_penalties)+"\n"
        self.previous_penalties=self.penalties

        
        for row in self.game.status()[0]:
            self.status+=str([card.n for card in row])+","
        self.status+=str([card.n for card in self.game.status()[2]])+","
        self.status+=str([card.n for card in self.hand])
 
        
        if len(self.hand)>0:
            cardIndexToPlay=random.randrange(0,len(self.hand))
            card=self.hand.pop(cardIndexToPlay)
            self.latest_played_card=card
            return card
    
    def resolveSmallNumberCard(self,card):
        """Handles a chosen card with a small number.

        The card triggers penalties from randomly chosen rows.

        Args:
            card (Card): The previously chosen card.
        """
        rowToTake=random.randrange(0,3)
        self.takePenalty(rowToTake,card)

    def takePenalty(self,rowIndex,card):   
        """Takes penalties from a row and updates player's penalty count.

        Args:
            rowIndex (int): Index of the row to replace with the new card.
            card (Card): The card that led to taking the penalties.
        """
        row=self.game.tableRows[rowIndex]
        penalties=[card.penalty for card in row]
        sumOfPenalties=sum(penalties)
        self.penalties+=sumOfPenalties
        self.game.removedCards+=self.game.tableRows[rowIndex]
        self.game.tableRows[rowIndex]=[card]
    
    def playAgain(self):
        """Determines whether the player wants to play again.

        Returns:
            bool: True to play again at the end of the game.
        """
        self.status+=","+str(self.latest_played_card.n)
        self.status+=","+str(self.penalties-self.previous_penalties)+"\n"
        self.latest_played_card=None
        self.latest_game_staus=[]
        self.n_games_performed+=1
        if self.n_games_performed%self.save_every==0:
            self.writeStatusOnFile()
        
        if self.n_games_performed<self.play_n_games:
            return True
        else:
            return False
    

    def writeStatusOnFile(self):
        file=open(self.file_output,"a")
        file.write(self.status)
        self.status=""
        file.close()
        
    def overwriteFile(self):
        file=open(self.file_output,"w")
        file.write("")
        file.close()
        