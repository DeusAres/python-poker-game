import random
import drawCard

class Player:
    def __init__(self, name='player', money=0, cards=None, bet=None, points=None):
        self.name = name
        self.cards = cards
        self.money = money
        self.bet = bet
        self.points = points
        self.allin = False
        self.minBet = None
        self.maxBet = None

    def betting(self, bet):
        if self.bet == None:
            self.bet = 0 

        if self.money < bet:
            bet = self.money
        self.money -= bet
        self.bet += bet
        if self.money == 0:
            self.allin = True

    def clear(self):
        self.cards = None
        self.bet = None
        self.minBet = None
        self.maxBet = None
        self.points = None
        self.allin = False

    def giveCards(self, deck):
        self.cards = deck.draw(2)




class Table:
    def __init__(self, blind, maxBet, cards=None, pot=0, points=None, allin=False):
        self.blind = blind
        self.cards = cards
        self.pot = pot
        self.points = points
        self.allin = allin

    def clear(self):
        self.cards = None
        self.pot = 0
        self.points=None
        self.allin = False

    def checkMinMaxBet(self, player, otherPlayers):
        """
        Updates min and max bet for player object
        player: Player object
        otherPlayers: List of Player objects
        """
        otherPlayersBets = [each.bet for each in otherPlayers]

        if None in otherPlayersBets or player.bet == None :
            if all([each == None for each in otherPlayersBets]):
                player.minBet = self.blind
                # Or player can check
                player.maxBet = min(*[each.money for each in otherPlayers], player.money)

            else:
                otherPlayersBets = [each for each in otherPlayersBets]
                otherPlayersBets = [0 if each == None else each for each in otherPlayersBets]

                player.minBet = self.blind if max(otherPlayersBets) == 0 else max(otherPlayersBets)

                player.maxBet = min([bet + each.money for bet, each in 
                    list(zip(*[[*otherPlayersBets,0], [*otherPlayers,player]]))])
            

        else:
            # Everyone has already betted, player included
            # consider that player betted 100, other better 200, 300, 400
            player.minBet = max(otherPlayersBets) - player.bet
            
            # Accounting all bets+money of players 
            player.maxBet = min(*[each.bet + each.money for each in otherPlayers], player.bet + player.money)


      
    
    def addToPot(self, players):
        self.pot = self.pot + sum([player.bet for player in players if player.bet != None])

        for i in range(len(players)):
            players[i].bet = None

    def payPlayer(self, player):
        player.money += self.pot
        self.pot = 0

    def isALLIN(self, players):
        if True in [player.allin for player in players]:
            self.allin = True

    def flop(self, deck):
        if self.cards == None:
            self.cards = deck.draw(3)
        elif len(self.cards) == 3 or len(self.cards) == 4:
            self.cards += deck.draw(1)

class Card:
    def __init__(self, number, suit, image=None):
        self.number = number
        self.suit = suit
        self.image = image

    def addImage(self):
        self.image = drawCard.main(self)

class  Deck:
    def __init__(self):

        numbers = [x for x in range(2,15)]
        deck = []

        for y in ["♥", "♦", "♣", "♠"]:
            for x in numbers:
                deck.append(Card(x, y))
        
        random.shuffle(deck)
        self.deck = deck

    def draw(self, number):
        drawn, self.deck = self.deck[:number], self.deck[number:]
        for i in range(len(drawn)):
            drawn[i].addImage()

        return drawn
    
    def remove(self, card):
        
        [self.deck.remove(each) for each in self.deck if card.number == each.number and card.suit == each.suit]