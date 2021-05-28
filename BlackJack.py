import random
"""
Have getters and setters for all values, Suit can be seperate class
"""
from abc import ABC
class Card(ABC):
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
        self.score = 0
    
    def draw(self,deck):
        self.hand.append(deck.drawCard())
    
    def showHand(self):
        for card in self.hand:
            card.show()
    # End of Deck of cards
    def score(self):
        for card in self.hand:
            self.score+= card.value
            
class BlackJackCard(Card):
    def __init__(self,suite,value):
        Card.__init__(self,suite,value)
    
    def value(self):
        if isAce(self.card):
            return 1
        elif faceCard():
            return 10
        else:
            return card.value
    
    def isAce(self,card):
        if card.value == 1:
            return True
    
    def faceCard(self,card):
        #number between 11 and 14 return True
        
            

class BlackJackHand(Player):
    
    def score(self):
        #if score > 21 and less than minOver minOver = score, similar for maxUnder
    
    def busted(self):
        return self.score() > 21
    
    def is21(self):
        #score is 21
            

deck = Deck()
deck.shuffle()

bob = Player("bob")
bob.draw(deck)
bob.showHand()
