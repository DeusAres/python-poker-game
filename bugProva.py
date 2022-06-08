from classes import *
import dealerCheck as dc

p = Player(cards=[Card(int(each[:-1]), each[-1]) for each in ["14♥", "13♥"]])
t = Table(None, None, cards=[Card(int(each[:-1]), each[-1]) for each in ["12♥", "11♥", "10♥", "14♠", "13♠"]])
print(dc.checkPoints(p, t))
