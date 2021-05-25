import random
import json
import functools
import sys


def rollDice():
    return random.sample([1, 2, 3, 4, 5, 6], 2)


def getBoard():
    data = [[{"count": 0, "type": None, 'str': ""} for i in range(12)] for i in range(5)]
    # data[0][0] = {"count": 5, "type": "y", 'str': "5y"}
    data[0][4] = {"count": 3, "type": "x", 'str': "3x"}

    data[0][6] = {"count": 5, "type": "x", 'str': "5x"}
    data[0][11] = {"count": 2, "type": "y", 'str': "2y"}

    # data[4][11] = {"count": 2, "type": "x", 'str': "2x"}
    # data[4][6] = {"count": 5, "type": "y", 'str': "5y"}

    # data[4][4] = {"count": 3, "type": "y", 'str': "3y"}
    # data[4][0] = {"count": 5, "type": "x", 'str': "5x"}

    data[2][4] = {"count": 3, "type": "y", 'str': "3x"} #xflanks
    data[2][7] = {"count": 3, "type": "y", 'str': "3y"} #yflanks

    data[2][5] = {"count": 0, "type": "y", 'str': "0"} #dice1
    data[2][6] = {"count": 0, "type": "y", 'str': "0"} #dice2


    data[2][8] = {"count": 0, "type": "y", 'str': "x"} #whose turn

    board = {
        "data": data,
        "turn": "x",
        "x": 11,
        "y": 5,
    }
    return board

def updateLog(log, end = "\n"):
    file = open("log.dat", "a")
    print(log, end = end, file=file)
    file.close()

def updateTable(board):
    file = open("table.dat", "w")
    printTable(board, file)
    file.close()

def printTable(board, file=sys.stdout):

    for i in "ABCDEFGHIJKL":
        print(f"{i:<5}", end='', file=file)
    print(file=file)
    for row in board["data"]:
        for cell in row:
            print(f"{cell['str']:<5}", end="", file=file)
        print(file=file)

def save(board):
    fp = open("dump.json", "w")
    json.dump(board, fp)
    fp.close()

def restore():
    fp = open("dump.json", "r")
    board = json.load(fp)
    return board

#3e3 becomes (3, 2, 4) (dice roll, rowNo, colNo)
def parse(source):
    parsed = ord(source[1]) - ord('a')
    return int(source[0]), int(source[2]) - 1, parsed


def checkWin(board, player = "x"):
    if player == "x":
        count = functools.reduce(lambda x, y: x + (y['count'] if y['type']=='x' else 0), board["data"][0][6:], 0)
        if count == board["x"]:
            return True
    else:
        count = functools.reduce(lambda x, y: x + (y['count'] if y['type']=='y' else 0), board["data"][4][6:], 0)
        if count == board["y"]:
            return True
    return False


def getDest(row, col, num, player = "", win = False):
    if win:
        return [row, col + num]
    dest = None
    if row == 0 and col - num < 0 and player == "y":
        dest = [4, 11 - (col- num)%12]

    elif row == 4 and col - num < 0 and player == "x":
        dest = [0, 11 - (col- num)%12]
    elif row == 0:
        dest = [row, col + (num if player=="x" else -num)]
    else:
        dest = [row, col - (num if player=="x" else -num)]

    
    if dest[1]<0 or dest[1] >= 12:
        print("invalid range", dest)
        return None
    return dest


def move(board, source, player = "x"):
    parsed = parse(source)
    row = parsed[1]
    col = parsed[2]
    num = parsed[0]
    win = checkWin(board, player)
    dest = getDest(row, col, num, player, win)

    if dest is None:
        return False

    fromCell = board["data"][row][col]

    if dest[1] >= 12:
        if fromCell["type"] != player or fromCell["count"] == 0:
            print(f"0 {player} found here")
            return False
        fromCell["count"] -= 1
        if fromCell["count"] == 0:
            fromCell["str"] = f""
            fromCell["type"] = None
        else:
            fromCell["str"] = f"{fromCell['count']}{fromCell['type']}"
        if player == "x":
            board["x"] -= 1
        elif player == "y":
            board["y"] -= 1
        board["data"][row][col] = fromCell
        return True



    toCell = board["data"][dest[0]][dest[1]]
    if fromCell["count"] == 0 or fromCell["type"] != player:
        print(f"0 {player} found here")
        return False

    elif toCell["type"] != player and toCell["count"] > 1:
        print(f"cell occupied by {toCell['str']}")
        return False

    elif toCell["type"] != player and toCell["count"] == 1:
        if player == "x":
            fromCell["count"] -= 1
            fromCell["str"] = f"{fromCell['count']}x"
            toCell["count"] = 1
            toCell["type"] = "x"
            toCell["str"] = "1x"
            board["data"][2][7]["count"] += 1
            board["data"][2][7]["str"] = f'{board["data"][2][7]["count"]}y'
        else:
            fromCell["count"] -= 1
            fromCell["str"] = f"{fromCell['count']}y"
            toCell["count"] = 1
            toCell["type"] = "y"
            toCell["str"] = "1y"
            board["data"][2][4]["count"] += 1
            board["data"][2][4]["str"] = f'{board["data"][2][4]["count"]}x'
        if fromCell["count"] == 0:
            fromCell["str"] = ""
            fromCell["type"] = None
        board["data"][row][col] = fromCell
        board["data"][dest[0]][dest[1]] = toCell
        print("finished moving")

    elif toCell["count"] == 0 or toCell["type"] == player:
        if player == "x":
            fromCell["count"] -= 1
            fromCell["str"] = f"{fromCell['count']}x"
            toCell["count"] += 1
            toCell["str"] = f"{toCell['count']}x"
            toCell["type"] = "x"
        else:
            fromCell["count"] -= 1
            fromCell["str"] = f"{fromCell['count']}y"
            toCell["count"] += 1
            toCell["str"] = f"{toCell['count']}y"
            toCell["type"] = "y"


        if fromCell["count"] == 0:
            fromCell["str"] = ""
            fromCell["type"] = None
        board["data"][row][col] = fromCell
        board["data"][dest[0]][dest[1]] = toCell
        print("finished moving last")
    else:
        return False
    return True


def flanksVar(board, player):
    if player == "x":
        return board["data"][2][4]["count"] > 0
    else:
        return board["data"][2][7]["count"] > 0

def canFlankBeMoved(board, rolls, player = "x"):
    cells = []
    if player == "x":
        cells = [board["data"][4][12-i] for i in rolls]
    else:
        cells = [board["data"][0][12-i] for i in rolls]
    for cell in cells:
        if cell["type"] == player or cell["count"] <= 1:
            return True
    print("Cannot be moved")
    return False


def moveFlank(board, rolls, player = "x"):
    playerstr = "Player 1" if player == "x" else "PLayer 2"
    dest = input(f"({playerstr}) Please choose destination for trapped {player}")
    parsed = parse(dest)
    num = parsed[0]
    row = parsed[1]
    col = parsed[2]

    if num not in rolls:
        print("Not in rolls")
        return False

    if player == "x":
        toCell = board["data"][4][12 - num]
    else:
        toCell = board["data"][0][12 - num]


    if toCell["count"] ==0 or toCell["type"] == player:
        toCell["count"] += 1
        toCell["type"] = player
        toCell["str"] = f"{toCell['count']}{player}"
        if player == "x":
            board["data"][2][4]["count"] -= 1
            board["data"][2][4]["str"] = f'{board["data"][2][4]["count"]}x'
        else:
            board["data"][2][7]["count"] -= 1
            board["data"][2][7]["str"] = f'{board["data"][2][7]["count"]}y'
        rolls.remove(num)
        return True
    
    elif toCell["count"] == 1:
        toCell["count"] = 1
        toCell["type"] = player
        toCell["str"] = f"{toCell['count']}{player}"
        if player == "x":
            board["data"][2][4]['count'] -= 1
            board["data"][2][4]['str'] = f"{board['data'][2][4]['count']}"
            board["data"][2][7]['count'] += 1
            board["data"][2][7]['str'] = f"{board['data'][2][7]['count']}"
        else:
            board["data"][2][7]['count'] -= 1
            board["data"][2][7]['str'] = f"{board['data'][2][7]['count']}"
            board["data"][2][4]['count'] += 1
            board["data"][2][4]['str'] = f"{board['data'][2][4]['count']}"
        rolls.remove(num)
        return True

    else:
        print("Cant move")
        return False

def movesVar(board, rolls, player = "x"):
    win = checkWin(board, player)
    for i in range(12):
        for ab in [0,4]:
            if board["data"][ab][i]["type"] == player and board["data"][ab][i]["count"] >0:
                for roll in rolls:
                    dest = getDest(ab, i, roll, player, win)
                    if dest is None:
                        continue
                    if dest[1] >= 12:
                        return True
                    toCell = board["data"][dest[0]][dest[1]]
                    if toCell["type"] == player or toCell["count"] <= 1:
                        return True
    return False