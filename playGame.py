import classes
import poker_gui as gui
import dealerCheck
import ia


class startOver(Exception):
    pass

class playerFold(Exception):
    pass

class comFold(Exception):
    pass

class endTurn(Exception):
    pass

def main(playerName, computerName, startingMoney, minBet):


    def newGame():
        player = classes.Player(playerName, startingMoney, None, 0, None)
        computer = classes.Player(computerName, startingMoney, None, 0, None)
        table = classes.Table(minBet, startingMoney)
        return player, computer, table

    def giveCards():
        # Deck is created
        deck = classes.Deck()

        # HERE WE SHOULD DECLARE TURN AND BASED ON THAT
        # PUT IF BIG BLIND OR SMALL BLIND

        # + Cards to player and Com
        # - Cards to deck
        player.giveCards(deck)
        computer.giveCards(deck)
        return deck

    def playerTurn():
        table.checkMinMaxBet(player, [computer])
        updateSliderAndText()

        if ((player.bet == None and computer.bet == None) or
            (computer.bet == 0 and player.bet == None)):
            gui.unlockCheck(window)
        else:
            gui.lockCheck(window)

        event, value = gui.readInput(window)
        gui.lockButtons(window)
        gui.lockCheck(window)

        if event == 'New Game':
            raise startOver
        if event == 'Fold':
            raise playerFold
        
        player.betting(value)
        updateText()
        gui.updateOut(window, actionDone(player, computer))
        
        if event == 'Bet':
            gui.playBet()
        elif event == 'Check':
            gui.playCheck()
        table.isALLIN([player, computer])
        gui.pause()

    def comTurn():

        table.checkMinMaxBet(computer, [player])

        action, bet = ia.main(computer, table, player)
        if action in ['Bet', 'Check']:
            computer.betting(bet)
        elif action == 'Fold':
            raise comFold

        updateText()
        if computer.bet == 0:
            gui.playCheck()
        else:
            gui.playBet()
        # End test

        gui.updateOut(window, actionDone(computer, player))
        gui.pause()
        pass

    def bettingTime():
        while True:
            for i in range(len(turn)):
                turn[i]()
                if (player.bet == computer.bet 
                    and player.bet != None 
                    and computer.bet != None):
                    raise endTurn

    def foldFunction():
        table.addToPot([player, computer])
        rewardWinner()
        updateText()

    def declareWinner():
        return dealerCheck.checkWinner(
            [player, computer], table)

    def rewardWinner():
        table.payPlayer([player, computer][winnerIndex])

    def updateSliderAndText():
        gui.updateBet(window, player)
        gui.updateText(window, player, computer, table)

    def updateText():
        gui.updateText(window, player, computer, table)

    def actionDone(p1, p2):
        if p1.money == 0 and p2.money != 0:
            return p1.name + " goes ALLIN with $" + str(p1.bet) + "!!!!"
        elif p1.money == 0 and p2.money == 0:
            return p1.name + " follows ALLIN with $" + str(p1.bet) + "!!!!"
        elif p1.bet == 0:
            return p1.name + " checks."
        elif p2.bet == None:
            return p1.name + " bets $" + str(p1.bet)
        elif p1.bet > p2.bet:
            return p1.name + " raises $" + str(p1.bet)
        elif p1.bet == p2.bet:
            return p1.name + " calls " + p2.name + " with $" + str(p1.bet)

    def clear():
        table.clear()
        player.clear()
        computer.clear()
        gui.clear(window)

    player, computer, table = newGame()
    winnerIndex = None

    turn = [lambda : comTurn(), lambda : playerTurn()]
    smallBlind = [lambda y,: y.betting(minBet), lambda y: y.betting(minBet*2)]
    smallFirst = [player, computer]
    window = gui.gameWindow(minBet, player, computer)
    
    while player.money != 0 and computer.money != 0:
        try:
            # Reset all the table
            clear()

            # Shuffle deck and give cards
            deck = giveCards()
            gui.giveCards(window, player)

            # Update GUI points
            player.points = dealerCheck.checkPoints(player, table)
            gui.updatePoints(window, player.points)

            smallBlind[0](smallFirst[0])
            updateText()
            gui.playBet()
            gui.pause()
            smallBlind[1](smallFirst[1])
            updateText()
            gui.playBet()
            gui.pause()

            turn.reverse()
            #smallBlind.reverse()
            smallFirst.reverse()

            table.isALLIN([player, computer])
            updateText()
            
            phase = ["Flop", "Turn", "River"]
            for i in range(3):
                if table.allin == False:
                    try:
                        bettingTime()
                    except endTurn:
                        updateText()
                        table.addToPot([player, computer])
                        updateText()
                        gui.updateOut(window, phase[i] + "!")
                
                table.flop(deck)
                gui.updateFlop(window, table)
                player.points = dealerCheck.checkPoints(player, table)
                gui.updatePoints(window, player.points)
                updateText()

            try:
                if table.allin == False:
                    bettingTime()
            except endTurn:
                updateText()

            table.addToPot([player, computer])

            # Flip COM cards
            gui.flipCOM(window, computer)

            # Checking winner
            winnerIndex = declareWinner()

            # Winning or losing interactive response
            player.points = dealerCheck.checkPoints(player, table)
            computer.points = dealerCheck.checkPoints(computer, table)
            gui.updateOut(window, 
                [player, computer][winnerIndex].name + " wins $" + str(table.pot) + " with " + 
                [player, computer][winnerIndex].points + "!!"
                )
            gui.playHand(winnerIndex)
            rewardWinner()
            updateText()

            # Waiting for continue or new game, analyze the table
            if gui.readInput(window, True)[0] == 'New Game':
                raise startOver


        except playerFold:
            winnerIndex = 1
            foldFunction()
            gui.playHand(winnerIndex)
            
        except comFold:
            winnerIndex = 0
            foldFunction()
            gui.playHand(winnerIndex)

    window.close()
    return None

"""
datas = gui.startGame()
if datas == 1:
    sys.exit(0)
"""
"""

"""
while True:
    try:
        """
        datas = gui.startGame()
        if datas == 1:
            break
        """
        datas = ["Nobody", "Skynet", 10000, 500]
        main(*datas)
        break
    except startOver:
        pass


    