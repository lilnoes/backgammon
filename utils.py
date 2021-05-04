import random
import json


def rollDice():
    return random.randint(1, 6)


def init():
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
    for i in range(12):
        print(f"{board['data'][i]['str']:<3}", end = '')
    print()

    for i in range(23, 11, -1):
        print(f"{board['data'][i]['str']:<3}", end = '')

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
    print(turn1, turn2)

def _toIndex(turn):
    if turn[1:] == '1':
        index = ord(turn[0]) - 97
        return index if 0 <= index < 12 else None

    index = 122 - ord(turn[0]) - 2
    return index if 23 >= index >= 12 else None


toIndex("e2 b2")
