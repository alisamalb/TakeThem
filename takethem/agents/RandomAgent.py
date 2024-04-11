import random

class RandomAgent:
    def __init__(self,game):
        self.game=game
        self.hand=[]
        self.penalties=0
        
    def draw(self,n=1):
        """Draw n cards from the deck of the game.

        Args:
            n (int, optional): Number of cards to draw. Defaults to 1.
        """
        if n==1:
            self.hand.append(self.game.deck.draw_card())
        else:
            self.hand+=self.game.deck.draw_cards(n)
        
    
    def playCard(self):
        """Mimics player's turn.
        "Plays" (returns) a random card from the hand.
        """
        cardIndexToPlay=random.randrange(0,len(self.hand))
        return self.hand.pop(cardIndexToPlay)