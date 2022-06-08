from classes import *
import dealerCheck
SUITS = ["♥", "♦", "♣", "♠"]

player = Player(cards = [
    Card(2, SUITS[2]),
    Card(9, SUITS[0]),
    
])

com = Player(cards = [
    Card(5, SUITS[1]),
    Card(8, SUITS[0])
])

tab = Table(None, None, cards = [
    Card(9 , SUITS[2]),
    Card(6, SUITS[3]),
    Card(8, SUITS[3]),
    Card(14, SUITS[3]),
    Card(14, SUITS[1]),
])


dealerCheck.checkWinner([player, com], tab)