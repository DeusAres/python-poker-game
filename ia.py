import random
import numpy as np
from classes import *

def winningStatistic(computer):

    # I was too lazy to study 2 players pocket hands winning statistic
    # I looked at a chart and came up with my statistics
    # Probably not accurate but seems good
    
    winning = 0
    start = 17; step = 1.9
    numberStat = [0,0] + np.arange(start, start+step*13, step).tolist()
    numbers = [each.number for each in computer.cards]

    if computer.cards[0].suit == computer.cards[1].suit:
        winning += 3

    winning += numberStat[numbers[0]] + numberStat[numbers[1]]

    if numbers[0] == numbers[1]:
        start = 20; stop = 2; step = (start-stop)/14; 
        add = [0,0] + np.arange(start,stop,-step).tolist()
        winning += add[numbers[0]]

    return winning

def almostPoker(hand, table):
    # Counting times a card appears
    numbers = [each.number for each in table.cards]
    numbers = {i:numbers.count(i) for i in numbers}

    inHand = [each.number for each in hand.cards]
    inHand = {i:inHand.count(i) for i in inHand}

    total = {k: numbers.get(k, 0) + inHand.get(k, 0) for k in set(numbers) | set(inHand)}

    # Excluding that Poker is in our hand
    if 4 in numbers.values():
        return "Poker on table", max(inHand.keys())

    # Excluding that Poker is on table
    elif 4 in total.values():
        return "Poker in hand", None

    # Excluding that there is a Full House on table
    elif 3 in numbers.values() and 2 in numbers.values():
        return "Full House on table", max(inHand.keys())
    
    elif 3 in numbers.values():
        return "Possible Poker", None

    elif 2 in numbers.values():
        possible = list(numbers.values()).count(2)
        blocked = 0
        for key, values in numbers.items():
            if values == 2 and inHand.get(key, None) == 1:
                blocked += 1

        if blocked == possible:
            return "Blocked Poker", None
        else:
            return "Improbable Poker", None

    return "No possible Poker", None

def almostStraight(hand, table):
    numbers = [each.number for each in table.cards]
    if 14 in numbers:
        numbers.append(1)
    # Reverse list sort
    numbers = list(dict.fromkeys(numbers))
    numbers.sort(reverse = True)

    improbable = False
    possible = False
    actuallyThereIs = False

    for i in range(14, 5, -1):
        count = 0
        for each in numbers:
            if each in list(range(i, i-5, -1)):
                count += 1
                
        
        # We know that there is a possible straight on the table
        if count in [3]:
            improbable = True
        if count in [4]:
            possible = True
        if count in [5]:
            actuallyThereIs = True

    if (possible or improbable) and not actuallyThereIs:
        
        # Let's sort and remove duplicates com hand and table
        total = [each.number for each in hand.cards] + numbers
        total = list(dict.fromkeys(total))
        total.sort(reverse = True)

        # Now we count how many pairs there are
        # At least 4 couples to make a straight
        # example: 12 23 34 45
        count_straight = 0
        for i in range(0, len(total)-1):
            if total[i]-1 == total[i+1]:
                count_straight +=1
            else:
                count_straight = 0

            if count_straight >= 4:
                # Writing down what's the scale
                straight = total[i-3 : i+2]

                return "Straight on hand", max(straight)
                # Or if the straight is in the table
            
        if possible:
            return "Possible Straight", None
        elif improbable:
            return "Improbable Straight", None

    if actuallyThereIs:
        # It's time to check if com has something for the straight
        hand = [each.numbers for each in hand.cards]

        # Check the highest card of the scale +1 is in com hand
        if table[0] + 1 in hand:
            if table[0] + 2 in hand:
                return "Straight on table and hand", table[0]+2
            return "Straight on table and hand", table[0]+1

        return "Straight on table", max(hand)
        
    return "No possible Straight", None

def almostFlush(hand, table):
    suits = [each.suit for each in table.cards]

    # Get a count of the suits on the table in a dict
    suits = {i:suits.count(i) for i in suits}

    # Get a count of the suits on table + hand in a dict
    add = [each.suit for each in hand.cards]
    total = suits.copy()
    for each in add:
        if each in total:
            total[each] += 1
        else:
            total[each] = 1


    # If 5 suits on table and got the suit in hand
    if 5 in suits.values():
        flushSuit = list(suits.keys())[list(suits.values()).index(5)]
        if flushSuit in add:
            maxTable = max([card.number for card in table.cards if card.suit == flushSuit])
            maxHand = max([card.number for card in hand.cards if card.suit == flushSuit])
            if maxTable < maxHand:
                return "Flush on table and max hand", max([card.number for card
                    in hand.cards if card.suit == flushSuit])
            else:
                return "Flush on table and hand", max([card.number for card in hand.cards 
                    if card.suit == flushSuit])
        else:
            return "Flush on table and highcard", max([card.number for card in hand.cards])

    # If sum of hand and table suit is >= to 5
    if True in [each >= 5 for each in total.values()]:
            return "Flush on hand", None

    # Table only
    if 4 in suits.values():
        
        return "Possible Flush", None
    
    # Table only
    if 3 in suits.values():
        return "Improbable Flush", None
    
    return "No possible Flush", None


def main(computer, table, player):
    if table.cards == None:
        winPerc = winningStatistic(computer)
        notFear = winPerc
        fear = notFear - 30

    else:
        fear = 1
        notFear = 1  
            
        result1, card1 = almostStraight(computer, table)
        result2, card2 = almostFlush(computer, table)
        result3, card3 = almostPoker(computer, table)

# STRAIGHT
        if result1 == 'Straight on hand':
            fear += 5
        elif result1 == "Straight on table and hand":
            fear += (100 / card1 - 7.14)
        elif result1 == "Straight on table":
            fear += (100 / card1)
        elif result1 == "Possible Straight":
            fear += 10
        elif result1 == 'Improbable Straight':
            fear += 5
        elif result1 == 'No possible Straight':
            fear += 0
# STRAIGHT

# FLUSH
        if result2 == 'Flush on table and max hand':
            fear -= 100
        elif result2 == 'Flush on table and hand':
            fear += (50 / card2)
        elif result2 == 'Flush on table and highcard':
            fear += (100 / card2)
        elif result2 == 'Flush on hand':
            fear -= 10
        elif result2 == 'Flush on table':
            fear += 20
        elif result2 == 'Possible Flush':
            fear += 10
        elif result2 == 'Improbable Flush':
            fear += 5
        elif result2 == 'No possible Flush':
            fear -= 20
# FLUSH

# POKER
        if result3 == 'Poker on table':
            fear += (100 / card3)
        elif result3 == 'Poker in hand':
            fear -= 100
        elif result3 == 'Full House on table':
            fear += (100 / card3)
        elif result3 == 'Possible Poker':
            fear += 50
        elif result3 == 'Blocked Poker':
            fear -= 20
        elif result3 == 'Improbable Poker':
            fear += 20
        elif result3 == "No possible Poker":
            fear -= 20
# POKER
        
# BET
    if fear < 0:
        notFear = 100-fear 
        fear = 1
    

    if player.bet not in [None, 0]:
        if player.money not in [None, 0]:
            fear /= (player.money / player.bet)
        
        action = random.choices(["Bet", "Fold"], weights=[notFear, fear],
            k=1)[0]

    else:
        action = random.choices(["Bet", "Check"], weights=[notFear, fear],
            k=1)[0]

    if action == 'Bet' and player.bet not in [None, 0]:
    
        available = [i for i in range(computer.minBet, computer.maxBet+1, table.blind)]
        scalingFear = notFear if notFear>1 else fear
        weights = [scalingFear/i for i in range(len(available), 0, -1)]
        weights.reverse()
        bet = random.choices(available, weights=weights,k=1)[0]
    
    else:
        bet = 0

    return action, bet
# If player.bet == 0 or None 
# Fear defines check
