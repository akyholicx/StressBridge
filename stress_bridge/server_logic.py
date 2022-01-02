import random, json, serializer

class Card(serializer.Serializable):
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit
    def getName():
        return f"{self.value}{self.suit}"

class Deck(serializer.Serializable):
    def __init__(self):
        self.cards = []

    def build(self):
        for value in range(1,14):
            for suit in ["c","d","h","s"]:
                card = Card(value,suit)
                self.cards.append(card)
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

class Player(serializer.Serializable):
    def __init__(self,name,position,points):
        self.position = position
        self.name = name
        self.hand = []
        self.points = points
        self.tricks = 0


class Game(serializer.Serializable):
    def __init__(self):
        self.deck = Deck()
        self.pile1 = Deck()
        self.pile2 = Deck()
        self.players = []
        self.deck.build()

    def addPlayer(self,player):
        self.players.append(player)

    def draw(self, name, count=1):
        if len(self.deck.cards) >= count:
            for i in range(count):
                card = self.deck.cards.pop()
                for player in self.players:
                    if player.name == name:
                        player.hand.append(card)

    def discard(self, name, index = 0):
        for player in self.players:
            if player.name == name:
                card = player.hand[index]
                player.hand.remove(card)
                pile = self.pile2.cards if player.position else self.pile1.cards
                pile.append(card)

'''
    def check(self):
        c1 = self.pile1.cards[-1]
        c2 = self.pile2.cards[-1]
        return c1.suit == c2.suit or c1.value == c2.value
'''

'''
game = Game()
game.addPlayer(Player("jon",0,0))
game.addPlayer(Player("keith",1,0))
game.draw("jon",26)
game.draw("keith",26)
game.discard("jon")
j = game.toJSON()
print(j)
'''

    
