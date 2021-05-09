import random
import json
import functools


def rollDice():
    return random.sample([1, 2, 3, 4, 5, 6], 2)


def getBoard():
    data = [[{"count": 0, "type": None, 'str': ""} for i in range(12)] for i in range(5)]
    data[0][0] = {"count": 5, "type": "y", 'str': "5y"}
    data[0][4] = {"count": 3, "type": "x", 'str': "3x"}

    data[0][6] = {"count": 5, "type": "x", 'str': "5x"}
    # data[0][11] = {"count": 2, "type": "y", 'str': "2y"}

    data[4][11] = {"count": 2, "type": "x", 'str': "2x"}
    # data[4][6] = {"count": 5, "type": "y", 'str': "5y"}

    # data[4][4] = {"count": 3, "type": "y", 'str': "3y"}
    data[4][0] = {"count": 5, "type": "x", 'str': "5x"}

    data[2][4] = {"count": 0, "type": "y", 'str': "0x"} #xflanks
    data[2][7] = {"count": 0, "type": "y", 'str': "0y"} #yflanks

    data[2][5] = {"count": 0, "type": "y", 'str': "0"} #dice1
    data[2][6] = {"count": 0, "type": "y", 'str': "0"} #dice2


    board = {
        "data": data,
        "turn": "x",
        "x": 15,
        "y": 15,
        "x_finished": False,
        "y_finished": False,
    }
    return board

def printTable(board):

    for i in "ABCDEFGHIJKL":
        print(f"{i:<5}", end='')
    print()
    for row in board["data"]:
        for cell in row:
            print(f"{cell['str']:<5}", end="")
        print()

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


def getDest(row, col, num, typea = ""):
    dest = None
    if row == 0 and col - num < 0 and typea == "y":
        dest = [4, 11 - (col- num)%12]

    elif row == 4 and col - num < 0 and typea == "x":
        dest = [0, 11 - (col- num)%12]
    elif row == 0:
        dest = [row, col + (num if typea=="x" else -num)]
    else:
        dest = [row, col - (num if typea=="x" else -num)]
    
    if dest[1]<0 or dest[1] >= 12:
        print("invalid range", dest)
        return None
    return dest


def move(board, source, typea = "x"):
    parsed = parse(source)
    row = parsed[1]
    col = parsed[2]
    num = parsed[0]
    dest = getDest(row, col, num, typea)

    if dest is None:
        return False

    fromCell = board["data"][row][col]
    toCell = board["data"][dest[0]][dest[1]]
    if fromCell["count"] == 0 or fromCell["type"] != typea:
        print(f"0 {typea} found here")
        return False

    elif toCell["type"] != typea and toCell["count"] > 1:
        print(f"cell occupied by {toCell['str']}")
        return False

    elif toCell["type"] != typea and toCell["count"] == 1:
        if typea == "x":
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

    elif toCell["count"] == 0 or toCell["type"] == typea:
        if typea == "x":
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


def flanksVar(board, typea):
    if typea == "x":
        return board["data"][2][4]["count"] > 0
    else:
        return board["data"][2][7]["count"] > 0

def canFlankBeMoved(board, rolls, typea = "x"):
    cells = []
    if typea == "x":
        cells = [board["data"][4][12-i] for i in rolls]
    else:
        cells = [board["data"][0][12-i] for i in rolls]
    for cell in cells:
        if cell["type"] == typea or cell["count"] <= 1:
            return True
    print("Cannot be moved")
    return False


def moveFlank(board, rolls, typea = "x"):
    dest = input(f"Please choose destination for trapped {typea}")
    parsed = parse(dest)
    num = parsed[0]
    row = parsed[1]
    col = parsed[2]

    if num not in rolls:
        print("Not in rolls")
        return False

    toCell = board["data"][4][12 - num]

    if toCell["count"] ==0 or toCell["type"] == typea:
        toCell["count"] += 1
        toCell["type"] = typea
        toCell["str"] = f"{toCell['count']}{typea}"
        if typea == "x":
            board["data"][2][4]["count"] -= 1
            board["data"][2][4]["str"] = f'{board["data"][2][4]["count"]}x'
        else:
            board["data"][2][7] -= 1
            board["data"][2][7]["str"] = f'{board["data"][2][7]["count"]}x'
        rolls.remove(num)
        return True
    
    elif toCell["count"] == 1:
        toCell["count"] = 1
        toCell["type"] = typea
        toCell["str"] = f"{toCell['count']}{typea}"
        if typea == "x":
            board["data"][2][4] -= 1
            board["data"][2][7] += 1
        else:
            board["data"][2][7] -= 1
            board["data"][2][4] += 1
        rolls.remove(num)
        return True

    else:
        print("Cant move")
        return False

def movesVar(board, rolls, typea = "x"):
    for i in range(12):
        for ab in [0,4]:
            if board["data"][ab][i]["type"] == typea and board["data"][ab][i]["count"] >0:
                for roll in rolls:
                    dest = getDest(ab, i, roll, typea)
                    if dest is None:
                        continue
                    toCell = board["data"][dest[0]][dest[1]]
                    if toCell["type"] == typea or toCell["count"] <= 1:
                        return True
    return False