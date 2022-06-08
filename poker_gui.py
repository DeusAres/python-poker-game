import PySimpleGUI as sg
import files
from pathlib import Path
from threading import Thread
from playsound import playsound
import sys
import time
from PIL import Image
import funPIL as df

SOUNDS = Path(__file__).parent / "sounds"
color, highlight, disabled = "#FF0000", "#FFFFFF", "#4a4a4a"
colors = color, highlight, disabled

sg.LOOK_AND_FEEL_TABLE["DarkPoker"] = {
    "BACKGROUND": "#252525",
    "TEXT": "#FFFFFF",
    "INPUT": "#af0404",
    "TEXT_INPUT": "#FFFFFF",
    "SCROLL": "#af0404",
    "BUTTON": ("#FFFFFF", "#252525"),
    "BORDER": 1,
    "SLIDER_DEPTH": 0,
    "PROGRESS_DEPTH": 0,
    "COLOR_LIST": ["#252525", "#414141", "#af0404", "#ff0000"],
    "PROGRESS": ("# D1826B", "# CC8019"),
}

sg.theme("DarkPoker")


def roundButtonImg(text, color, highlight, disabled, visible=True):
    w, h = df.getSize(text, df.fontDefiner("C:\\Windows\\Fonts\\Arial.ttf", 20))
    w += 30
    h += 20

    OUT = df.backgroundPNG(w * 5, h * 5, color)
    OUT[0] = df.roundCorners(OUT[0], 4 * 5)
    IN = df.replaceColor(OUT[0], color, highlight).resize(
        (w, h), resample=Image.ANTIALIAS
    )
    DISABLED = df.replaceColor(OUT[0], color, disabled).resize(
        (w, h), resample=Image.ANTIALIAS
    )
    OUT = OUT[0].resize((w, h), resample=Image.ANTIALIAS)
    OUT, IN, DISABLED = [df.image_to_data(each) for each in [OUT, IN, DISABLED]]

    button = sg.Button(
        text,
        border_width=0,
        button_color=sg.theme_background_color(),
        disabled_button_color=sg.theme_background_color(),
        image_data=OUT,
        visible=visible,
    )

    return button, IN, OUT, DISABLED


buttons = {
    # "START" : [*roundButtonImg('START', *colors)],
    "Bet": [*roundButtonImg("Bet", *colors)],
    "Check": [*roundButtonImg("Check", *colors)],
    "Fold": [*roundButtonImg("Fold", *colors)],
    "New Game": [*roundButtonImg("New Game", *colors)],
    "Continue": [*roundButtonImg("Continue", *colors, False)],
}


def in_out(window, event, buttonDict):
    if "+IN+" in event:
        element = event.replace("+IN+", "")
        if window[element].Disabled == "ignore":
            return True
        window[element].Update(
            button_color=(color, sg.theme_background_color()),
            image_data=buttonDict[element][1],
        )
        window.refresh()
        return True
    elif "+OUT+" in event:
        element = event.replace("+OUT+", "")
        if window[element].Disabled == "ignore":
            return True
        window[element].Update(
            button_color=(highlight, sg.theme_background_color()),
            image_data=buttonDict[element][2],
        )
        window.refresh()
        return True
    return False


def disable(window, element, disabled):
    if disabled:
        state, index = sg.BUTTON_DISABLED_MEANS_IGNORE, 3
    else:
        state, index = False, 2

    window[element].Update(
        button_color=(highlight, sg.theme_background_color()),
        disabled=state,
        image_data=buttons[element][index],
    )
    window.refresh()


def startGame():
    buttons2 = {
        "START": [*roundButtonImg("START", *colors)],
    }
    startGameGUI = [
        [
            sg.Column(
                [
                    [sg.Text("Player Name")],
                    [sg.Text("Computer Name")],
                    [sg.Text("Starting Money")],
                    [sg.Text("Minimal Bet")],
                ]
            ),
            sg.Column(
                [
                    [sg.Input("Nobody", key="PLAYERNAME")],
                    [sg.Input("Skynet", key="COMPUTERNAME")],
                    [sg.Input(str(10000), key="STARTINGMONEY")],
                    [sg.Input(str(500), key="MINBET")],
                ]
            ),
        ],
        [sg.Push(), buttons2["START"][0], sg.Push()],
    ]

    window = sg.Window("Poker", startGameGUI, use_default_focus=False, finalize=True)
    [
        window["START"].bind(*each)
        for each in [("<Enter>", "+IN+"), ("<Leave>", "+OUT+")]
    ]

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == "Quit":
            break

        if in_out(window, event, buttons2):
            continue

        if event == "START":
            playerName, computerName, startingMoney, minBet = (
                values["PLAYERNAME"].strip("\n").strip(" "),
                values["COMPUTERNAME"].strip("\n").strip(" "),
                values["STARTINGMONEY"].strip("\n").strip(" "),
                values["MINBET"].strip("\n").strip(" "),
            )

            if startingMoney.isdigit() and minBet.isdigit():
                startingMoney, minBet = int(startingMoney), int(minBet)
                if startingMoney > minBet:
                    window.close()
                    return playerName, computerName, startingMoney, minBet

    window.close()
    return 1


def gameWindow(minBet, player, computer):

    for each in buttons:
        visible = False if each == "Continue" else True
        buttons[each][0] = sg.Button(
            each,
            border_width=0,
            button_color=sg.theme_background_color(),
            disabled_button_color=sg.theme_background_color(),
            image_data=buttons[each][2],
            visible=visible,
        )

    font = ("Arial", 20, ["bold"])
    minifont = ("Arial", 10, ["bold"])
    layout = [
        # COM SIDE
        [
            sg.Push(),
            sg.Text(
                computer.name,
                text_color="#FF0000",
                font=font,
            ),
            sg.Text(
                "$" + str(computer.money),
                text_color="#FF0000",
                font=minifont,
                key="COMMONEY",
            ),
            sg.Text(
                "$0",
                text_color="#FF0000",
                font=font,
                key="COMBET"
            ),
            sg.Push()
        ],
        [
            sg.Push(),
            *[
                sg.Image(data=files.placeHolder, key="C_" + str(each), p=((5, 5),(20,20)))
                for each in list(range(1, 3))
            ],
            sg.Push(),
        ],
        [
            sg.Push(), 
            sg.Text(
                "TABLE POT: ",
                text_color="#FF0000",
                font=font
            ), 
            sg.Text(
                "$0", 
                key="TABLEPOT",
                text_color="#FF0000",
                font=font
            ), 
            sg.Push()
        ],
        # TABLE SIDE
        [
            sg.Push(),
            [
                sg.Image(data=files.placeHolder, key="T_"+str(each), p=((5, 5),(20,20)))
                for each in [1, 2, 3, 4, 5]
            ],
            sg.Push(),
        ],

        # PLAYER SIDE
        [
            sg.Push(),
            *[
                sg.Image(data=files.placeHolder, key="P_" + str(each), p=((5, 5),(20,20)))
                for each in list(range(1, 3))
            ],
            sg.Push(),
        ],

        [
            sg.Push(),
            sg.Text(
                player.name, 
                text_color="#FF0000", 
                font=font
            ),
            sg.Text(
                "$" + str(player.money),
                text_color="#FF0000",
                font=minifont,
                key="PLAYERMONEY",
            ),
            sg.Text(
                "$0", 
                text_color="#FF0000",
                font=font,
                key="PLAYERBET"
            ),
            sg.Push(),
        ],

        [
            sg.Push(),
            sg.Slider(
                range=(None, None),
                default_value=None,
                resolution=minBet,
                orientation="horizontal",
                key="BET",
            ),
            *[buttons[each][0] for each in ["Bet", "Check", "Fold"]],
            sg.Push(),
        ],
        
        [sg.Push(), sg.Text("YOU GOT: "), sg.Text("", key="POINTS"), sg.Push()],
        [sg.Push(), sg.Text("PLAYING...", key="OUT"), sg.Push()],
        [sg.Push(), sg.pin(buttons["Continue"][0]), sg.Push()],
        [sg.Push(), sg.pin(buttons["New Game"][0])],
    ]

    window = sg.Window("Poker", layout, use_default_focus=False, finalize=True)
    for button in buttons.keys():
        [
            window[button].bind(*each)
            for each in [("<Enter>", "+IN+"), ("<Leave>", "+OUT+")]
        ]
    return window


def readInput(window, keepLock=False):
    event = None
    # while event != 'Check' and event != 'Bet' and event != 'Continue' and event != 'Fold':
    if keepLock == False:
        unlockButtons(window)
    while event not in ["Check", "Bet", "Continue"]:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == "Quit":
            sys.exit(0)

        if in_out(window, event, buttons):
            continue

        if event == "Check":
            playCheck()
            value = 0
        elif event == "Bet":
            playBet()
            value = int(values["BET"])
        elif event == "Fold" or event == "Continue" or event == "New Game":
            if event == "Continue":
                window["Continue"].Update(visible=False)
                unlockButtons(window)
            value = None
            if event == "New Game":
                window.close()
                del window
            return event, None

    lockButtons(window)
    return event, value


def giveCards(window, player):

    # Updating GUI of player
    display = ["P_1", "P_2"]

    for element, card in list(zip(*[display, player.cards])):
        t = Thread(target=playFlip, args=())
        t.start()
        window[element].Update(data=card.image)
        t.join()
        window.refresh()

    # Updating GUI of COM with facedown cards
    display = ["C_1", "C_2"]
    [window[element].Update(data=files.cardBack) for element in display]

    # Updating GUI of table
    [
        window["T_" + str(each)].Update(data=files.placeHolder)
        for each in [1, 2, 3, 4, 5]
    ]


def flipCOM(window, computer):

    # Updating GUI of COM flipping his cards
    t = Thread(target=playFlip, args=())
    t.start()
    display = ["C_1", "C_2"]
    [
        window[element].Update(data=card.image)
        for element, card in list(zip(*[display, computer.cards]))
    ]
    window.refresh()
    t.join()
    lockButtons(window)
    window["Continue"].Update(visible=True)


def updateFlop(window, table):

    if len(table.cards) == 3:
        rangeIndex = [1, 2, 3]
    elif len(table.cards) == 4:
        rangeIndex = [4]
    elif len(table.cards) == 5:
        rangeIndex = [5]

    for each in rangeIndex:
        t = Thread(target=playFlip, args=())
        t.start()
        window["T_" + str(each)].Update(data=table.cards[each - 1].image)
        window.refresh()
        t.join()


def updateBet(window, player):
    window["BET"].Update(range=(player.minBet, player.maxBet))
    window.refresh()


def updateText(window, player, computer, table):

    datas = [player.bet, player.money, computer.bet, computer.money, table.pot]
    datas = ["$" + str(each) if type(each) == int else str("None") for each in datas]

    for i in range(len(datas) - 1):
        if datas[i] == "$0":
            # Bet data index
            if i % 2 == 0:
                datas[i] = datas[i].replace("$0", "CHECK")
            # Money data index
            else:
                datas[i] = datas[i].replace("$0", "ALLIN")

    elements = ["PLAYERBET", "PLAYERMONEY", "COMBET", "COMMONEY", "TABLEPOT"]

    [
        window[element].Update(str(data))
        for element, data in list(zip(*[elements, datas]))
    ]

    window.refresh()


def updateOut(window, message):
    window["OUT"].Update(message)
    window.refresh()


def updatePoints(window, points):
    window["POINTS"].Update(points)
    window.refresh()


def lockCheck(window):
    disable(window, "Check", True)
    window.refresh()


def unlockCheck(window):
    disable(window, "Check", False)
    window.refresh()


def unlockButtons(window):
    elements = ["Bet", "Fold"]
    [disable(window, each, False) for each in elements]
    window.refresh()


def lockButtons(window):
    elements = ["Bet", "Fold"]
    [disable(window, each, True) for each in elements]
    window.refresh()


def clear(window):
    elements = ["C_" + str(i) for i in range(1, 3)]
    elements += ["P_" + str(i) for i in range(1, 3)]
    elements += ["T_" + str(i) for i in range(1, 6)]
    [window[each].Update(data=files.placeHolder) for each in elements]
    # [window["T_"+str(each)].Update(data=files.placeHolder) for each in list(range(1,6))]


def playFlip():
    # folding card sound
    # Path(__file__).parent / sounds
    playsound(str(SOUNDS / "flip.mp3"))


def playWinHand():
    playsound(str(SOUNDS / "win.mp3"))


def playLostHand():
    playsound(str(SOUNDS / "lose.mp3"))
    pass


def playHand(winnerIndex):

    if winnerIndex == 0:
        t = Thread(target=playWinHand, args=())
    elif winnerIndex == 1:
        t = Thread(target=playLostHand, args=())

    t.start()
    t.join()


def playBet():
    # playsound(str(SOUNDS /"chips.mp3"))

    t = Thread(target=playsound, args=(str(SOUNDS / "chips.mp3"),))
    t.start()


def playCheck():
    t = Thread(target=playsound, args=(str(SOUNDS / "check.mp3"),))
    t.start()


def pause():
    time.sleep(1.5)
