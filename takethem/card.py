class Card:
    def __init__(self,n):
        "Initializes card with number n"
        self.n=n
        self.penalty=self._calculate_penalty()
        self.lastOwner=None
        
    def _calculate_penalty(self):
        """Each card has a penalty assosicated,
        based on its number."""
        if (self.n%55)==0:
            return 7
        if (self.n%11)==0:
            return 5
        if (self.n%10)==0:
            return 3
        if (self.n%5)==0:
            return 2
        return 1
    
    def setOwner(self,owner):
        """Takes note of the player's hand
        it belongs to.
        
        owner: Player intance.
        """
        self.lastOwner=owner