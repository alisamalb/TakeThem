import random
from .card import Card

class Deck:
    def __init__(self,n):
        "Initializes a new deck with n cards"
        self.deck=[Card(i+1) for i in range(n)]
        self._shuffle()
        
    def _shuffle(self):
        "Shuffles the deck"
        random.shuffle(self.deck)
        
    def draw_card(self):
        """Draw the card from the top of the deck
           and returns it."""
        return self.deck.pop()
    
    def draw_cards(self,howmany=1):
        """Draws multiple cards from the top of the
        deck and returns them as a list."""
        cards=[self.draw_card() for x in range(howmany)]
        return cards
        