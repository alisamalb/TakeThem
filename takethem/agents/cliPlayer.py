class cliPlayer:
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
        Asks for user input and "plays" (returns) a card.
        """
        cardIndexToPlay=42
        while cardIndexToPlay>len(self.hand):
            userInput=input(f"Which card do you want to play? (enter number 1-{len(self.hand)})\n")
            try:
                int(userInput)
            except:
                print(f"That is not a valid integer.")
                userInput=42

            if int(userInput)>len(self.hand):
                print(f"The chosen number is too large. Max is {len(self.hand)}")
            
            else:
                cardIndexToPlay=int(userInput)-1
                return self.hand.pop(cardIndexToPlay)