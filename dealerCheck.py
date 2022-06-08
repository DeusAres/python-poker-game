POINTS = ["ROYALFLUSH", "STRAIGHTFLUSH", "FOUROFAKIND", "FULL", "FLUSH", "STRAIGHT", "TRIPLE", "TWOPAIRS", "ONEPAIR", "HIGHCARD"]
SUITS = ["♥", "♦", "♣", "♠"]

def checkPoints(player, table):

    a = player.cards.copy()
    if table != None and table.cards != None:
        a += table.cards.copy()
    numbers, suits = list(zip(*[[each.number, each.suit] for each in a]))
    numbers, suits = list(numbers), list(suits)
    numbers.sort()

    if 14 in numbers:
        numbers.insert(0, 1)
    coppie = {i:numbers.count(i) for i in numbers}

    HIGHCARD = True
    ONEPAIR = True if 2 in coppie.values() else False

    if table.cards == None:
        for value, name in list(zip(*[[ONEPAIR, HIGHCARD], ['ONEPAIR', 'HIGHCARD']])):
            if value == True:
                return name

    TWOPAIRS = True if list(coppie.values()).count(2) >= 2 else False

    TRIPLE = True if 3 in coppie.values() else False

    count = 0
    duplicates = 0
    index = 0
    a.sort(key=lambda x: x.number, reverse=True)
    rSortedTable = a

    for i in range(0, len(rSortedTable)-1):
        if rSortedTable[i].number-1 == rSortedTable[i+1].number:
            count +=1 
        elif rSortedTable[i].number == rSortedTable[i+1].number:
            duplicates += 1
            continue

        else:
            if count >= 4:
                break
            count = 0
            index = i+1
        
    STRAIGHT = True if count >= 4 else False

    #colorCount = max(*[suits.count(s) for s in ["♠", "♥", "♦", "♣"]])
    suitsDict = {i:suits.count(i) for i in suits}
    FLUSH = True if sum([each in suitsDict.values() for each in [5,6,7]]) else False
    
    FULL = True if list(coppie.values()).count(3) >= 2 else False
    FULL = True if 3 in coppie.values() and 2 in coppie.values() else False

    FOUROFAKIND = True if 4 in coppie.values() else False

    ROYALFLUSH = False
    STRAIGHTFLUSH = False

    if STRAIGHT and FLUSH:
        straight = rSortedTable[index:index+count+duplicates+1]
        flushSuit = list(suitsDict.keys())[list(suitsDict.values()).index(max(list(suitsDict.values())))]
        straight = [card for card in straight if card.suit == flushSuit]
        if len(straight) >= 5:
            if straight[0].number == 14 and straight[-1].number == 10:
                ROYALFLUSH = True
            else:
                STRAIGHTFLUSH = True

    

    value = [[ROYALFLUSH, STRAIGHTFLUSH, FOUROFAKIND, FULL, FLUSH, STRAIGHT, TRIPLE, TWOPAIRS, ONEPAIR, HIGHCARD]]
    name = [POINTS]
    for value, name in list(zip(*value+name)):
        if value == True:
            return name

"""
def checkHighestCard(player, pc):
    playerNumbers = [each.number for each in player.cards]
    pcNumbers = [each.number for each in pc.cards]
    
    playerMax, pcMax = max(playerNumbers), max(pcNumbers)



    if playerMax > pcMax: #HIGHEST CARD ON PLAYER
        return (0,1) #PLAYER WINS

    elif playerMax == pcMax: #SAME HIGHEST CARD
        playerMin, pcMin = min(playerNumbers), min(pcNumbers)

        if playerMin > pcMin: #LOWEST HIGHEST CARD ON PLAYER
            return (0,1) #PLAYER WINS

        elif playerMin == pcMin: #SPLITTED POKER CHECKING SUITS
            if all([playerMin == each for each in [playerMax, pcMin, pcMax]]):
                suits = ["♥", "♦", "♣", "♠"]
                playerSuit = suits.index([each.suit for each in player.cards])
                pcSuit = suits.index([each.suit for each in player.cards])
                if playerSuit > pcSuit:
                    return (0,1) #PLAYER WINS
                else:
                    return (1,0) #PC WINS

        if playerMin < pcMin: #LOWEST HIGHEST CARD ON PC
            return (1,0) #PCWINS

    elif playerMax < pcMax: #LOWEST HIGHEST CARD ON PC
        return (1,0) #PC WINS
"""
def checkHighestCard(players, indices):
    newPlayers = []
    maxNew, minNew = [], []
    for i in range(len(players)):
        if i in indices:
            newPlayers.append([card.number for card in players[i].cards])
        else:
            newPlayers.append([0,0])
        maxNew.append(max(newPlayers[i]))
        minNew.append(min(newPlayers[i]))
    
    # Get highest of the table
    maxTable = max(maxNew)
    
    if maxNew.count(maxTable) > 1:
    # Another draw of the max

        # Get highest of lowest
        maxMinTable = max(minNew)

        # Another draw
        if minNew.count(maxMinTable):

            # Let's get the players with maxTable in hand
            # and extract the suits
            winner = []
            for i in range(len(players)):
                if i in indices:
                    numbers = [card.number for card in players[i].cards]
                    if maxTable in numbers:
                        suits = [card.suit for card in players[i].cards]
                        winner.append(min([SUITS.index(each) for each in suits]))
                else:
                    winner.append(10)

            return winner.index(0)

    else:
        return maxNew.index(maxTable)
    
def checkFlushDraw(players, table, indices):

    suits = [card.suit for card in table.cards]
    suits = {i:suits.count(i) for i in suits}

    # Get the suit of flush
    flushSuit = max(list(suits.values()))
    flushSuit = list(suits.keys())[flushSuit]

    # Create a new list of cards only of suits
    playersSuit = []
    for i in range(len(players)):
        if i == indices:
            playersSuit.append([card.number if card.suit == flushSuit else 0 
                                for card in players[i].cards ])

    # Get max card
    for i in range(len(playersSuit)):
           playersSuit[i] = max(playersSuit[i])

    if all(each == 0 for each in playersSuit):
        return indices
    else:
        return playersSuit.index(max(playersSuit))

def checkStraightDraw(players, table, indices):

    totalPlayers = [players[i].cards + table.cards if i in indices else 0
                    for i in range(len(players)) ]

 
    for i in range(len(totalPlayers)):
        if totalPlayers[i] != 0:
            numbers = [card.number for card in totalPlayers[i]]
            numbers = list(dict.fromkeys(numbers))
            numbers.sort(reverse=True)

            count = 0
            for i in range(len(numbers)-1):
                if numbers[i]-1 == numbers[i+1]:
                    count += 1
                else:
                    count = 0

                if count == 4:
                    totalPlayers[i] = max(numbers[i-4])
                    break
                

    highest = max(totalPlayers)
    if totalPlayers.count(highest) > 1:
        return [i for i, x in enumerate(totalPlayers) if x == highest]
    elif totalPlayers.count(highest) == 0:
        return indices
    else:
        return totalPlayers.index(max(totalPlayers))

def checkFullDraw(players, table, indices):
    triple = []
    double = []
    for i in range(len(players)):
        if i in indices:
            total = players[i].cards + table[i].cards
            total = [card.number for card in total]
            total = {i:total.count(i) for i in total}

            tempTriple = [key for key,value in total.items() if value == 3]
            try:
                triple.append(max(tempTriple))
            except:
                triple.append(0)
                double.append(0)
                continue

            tempDouble = [key for key,value in total.items() if value >= 2 and key != tempTriple]
            try:
                double.append(max(tempDouble))
            except:
                double.append(0)
            
        else:
            total.append([0,0])
        
    indices = [i for i, x in enumerate(triple) if x == max(triple)]
    if len(indices) > 1:
        indices = [i for i, x in enumerate(triple) if x == max(double) and i in indices]
        if len(indices) > 1:
            return indices
        else:
            return indices[0]

    else:
        return indices[0]


def checkWinner(players, table):
            
    playersScore = [checkPoints(player, table) for player in players]
    playersScore = [POINTS.index(each) for each in playersScore]
    bestHand = min(playersScore)
    isItDraw = True if playersScore.count(bestHand) > 1 else False

    
    if isItDraw:

        indices = [i for i, x in enumerate(playersScore) if x == bestHand]
       

        if bestHand in ['FLUSH', 'STRAIGHTFLUSH']:
            result = checkFlushDraw(players, table, indices)
            
        elif bestHand == 'STRAIGHT':
            result = checkStraightDraw(players, table, indices)
        
        elif bestHand == 'FULL':
            result = checkFullDraw(players, table, indices)
        else:
            result = indices

        if type(result) == list:
            result = checkHighestCard(players, result)
        
    else:
        result = playersScore.index(bestHand)
    
    return result






   
   
   