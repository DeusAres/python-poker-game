import random


    

def printCards(text, hand):
    replacing = ['T', 'J', 'Q', 'K', 'A']
    numbers = [10, 11, 12, 13, 14]

    replaced = []

    for card in hand.cards:
        if card.number in numbers:
            replaced.append(str(replacing[numbers.index(card.number)]) + card.suit)
        else:
            replaced.append(str(card.number) + card.suit)

    print(text, " ".join(replaced))
            
       

"""
player = Player(10000, 0, None)
pc = Player(10000, 0, None)
table = Table(0, None)

def do():
    dealer = Deck()
    player.giveCards(dealer.draw(2))
    pc.giveCards(dealer.draw(2))

    table.flop(dealer.draw(5))#table.flop([Card(i, '♥') for i in range(2, 7)])

def did():
    replacing = ['T', 'J', 'Q', 'K', 'A']
    numbers = [10, 11, 12, 13, 14]
    a,b,c = PC 2♦ 9♦
TABLE 6♣ 7♠ Q♣ 7♣ A♦
ME 4♦ 5♥.split('\n')

    a = a.replace("PC ", '')
    b = b.replace("TABLE ", '')
    c = c.replace("ME ", '')


    def man(c):
        c = c.split(' ')
        new = []
        for each in c:
            if each[0] in replacing:
                index = replacing.index(each[0])
                new.append([each[0].replace(replacing[index], str(numbers[index])), each[1]])
            else:
                new.append([each[0], each[1]])
        new = [Card(int(x[0]), x[1]) for x in new]
        return new

    man(a)
    man(b)
    table.flop(man(b))
    pc.giveCards(man(a))
    player.giveCards(man(c))
    

while True:
    do()

    printCards("PC", pc)
    printCards("TABLE", table)
    printCards("ME", player)
    pcScore, playerScore = checkPoints(pc, table), checkPoints(player, table)
    print("PC GOTS:", pcScore)
    print("I GOT:", playerScore)


    values = ["POKER", "FULL", "COLOR", "STRAIGHT", "TRIPLE", "TWOPAIRS", "ONEPAIR", "HIGHCARD"]
    pcIndex = values.index(pcScore)
    playerIndex = values.index(playerScore)

    if playerIndex == pcIndex:
        playerIndex, pcIndex = checkHighestCard(player, pc)
    if playerIndex < pcIndex:
        print("PLAYER WINS")
    else:
        print("PC WINS!")
        
    input("New hand >")
"""