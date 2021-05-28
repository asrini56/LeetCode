import random
"""
Have getters and setters for all values, Suit can be seperate class
"""

class Card:
    def __init__(self,suit,value):
        self.suit = suit
        self.value = value
    
    def show(self):
        #show what card it is

class Deck:
    def __init__(self):
        self.cards = []
        self.build()
    
    def build(self):
        for s in ["S","D","C","H"]:
            for i in range(len(1,14)):
                self.cards.append(Card(s,i))

    def show(self):
        #Show all cards
    
    def shuffle(self):
        #random.shuffle(self.cards) or
        for i in range(len(self.cards)-1,0,-1):
            r = random.randint(0,i)
            self.cards[i], self.cards[r] = self.cards[r],self.cards[i]
    
    def drawCard(self):
        return self.cards.pop()

class Player:
    def __init__(self,name):
        self.name = name
        self.hand = []
    
    def draw(self,deck):
        self.hand.append(deck.drawCard())
    
    def showHand(self):
        for card in self.hand:
            card.show()

deck = Deck()
deck.shuffle()

bob = Player("bob")
bob.draw(deck)
bob.showHand()
