import random
import json


def rollDice():
    return random.sample([1, 2, 3, 4, 5, 6], 2)


def getBoard():
    data = [{"count": 0, "type": "", 'str': ""} for i in range(6+6+6+6)]
    data[0] = {"count": 5, "type": "y", 'str': "5y"}
    data[4] = {"count": 3, "type": "x", 'str': "3x"}

    data[6] = {"count": 5, "type": "x", 'str': "5x"}
    data[11] = {"count": 2, "type": "y", 'str': "2y"}

    data[12] = {"count": 2, "type": "x", 'str': "2x"}
    data[17] = {"count": 5, "type": "y", 'str': "5y"}

    data[19] = {"count": 3, "type": "y", 'str': "3y"}
    data[23] = {"count": 5, "type": "x", 'str': "5x"}


    board = {
        "data": data,
        "x_flank": 0,
        "y_flank": 0,
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
    for i in range(12):
        cell = board['data'][i]
        print(f"{board['data'][i]['str']:<5}", end = '')
    print()

    for i in range(23, 11, -1):
        print(f"{board['data'][i]['str']:<5}", end = '')
    print()
    # for i in "ABCDEFGHIJKL":
        # print(f"{i:<5}", end='')
    # print()

def save(board):
    fp = open("dump.json", "w")
    json.dump(board, fp)
    fp.close()

def restore():
    fp = open("dump.json", "r")
    board = json.load(fp)
    return board

def toIndex(turns):
    turn1, turn2 = turns.split(" ")
    if turn1[1:] != turn2[1:]:
        return None
    turn1 = _toIndex(turn1)
    turn2 = _toIndex(turn2)
    # print(turn1, turn2)
    return turn1, turn2

def _toIndex(turn):
    if turn[1:] == '1':
        index = ord(turn[0]) - 97
        return index if 0 <= index < 12 else None

    index = 122 - ord(turn[0]) - 2
    return index if 23 >= index >= 12 else None

def move(board, source, num, typea = "x"):
    num = num if typea=="x" else -num

    fromCell = board["data"][source]
    toCell = board["data"][(source + num) % 24]
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
            board["y_flank"] += 1
        else:
            fromCell["count"] -= 1
            fromCell["str"] = f"{fromCell['count']}y"
            toCell["count"] = 1
            toCell["type"] = "y"
            toCell["str"] = "1y"
            board["x_flank"] += 1
        board["data"][source] = fromCell
        board["data"][(source + num) % 24] = toCell
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
        if toCell["count"] == 0:
            toCell["str"] = ""
        board["data"][source] = fromCell
        board["data"][(source + num) % 24] = toCell
        print("finished moving last")
    else:
        return False
    return True


# toIndex("e2 b2")
