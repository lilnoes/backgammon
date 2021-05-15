import utils

print(utils.getDest(0, 0, 1, "y"))

# board = utils.getBoard()
board = utils.restore()
typea = board['data'][2][8]['str']
typea = "x" if typea == "y" else "y"

while True:
    if board["x"] == 0:
        print("X won")
        break
    elif board["y"] == 0:
        print("Y won")
        break
    typea = "y" if typea == "x" else "x"
    board['data'][2][8]['str'] = typea
    utils.save(board)
    print("Rolling...")
    rolls = utils.rollDice()
    # rolls = [1,1]
    board["data"][2][5]["str"] = str(rolls[0])
    board["data"][2][6]["str"] = str(rolls[1])
    print(f"{typea} turn")
    print(f"Rolled {rolls[0]} and {rolls[1]}")
    rolls = rolls + rolls if rolls[0] == rolls[1] else rolls
    while len(rolls) != 0:
        print("rolls", rolls)
        utils.printTable(board)
        if utils.flanksVar(board, typea):
            if not utils.canFlankBeMoved(board, rolls, typea):
                print("Can not be moved, going to next player")
                break
            utils.moveFlank(board, rolls, typea)
            continue
        if not utils.movesVar(board, rolls, typea):
            print("No moves available, next player")
            break
        else:
            player = "Player 1" if typea == "x" else "PLayer 2"
            source = input(f"({player}) Please choose source: ")
            dest = utils.parse(source)
            if dest[0] not in rolls:
                print(f"{dest[0]} not in rolled numbers")
            elif not utils.move(board, source, typea):
                print("TRy again, you can do it")
            else:
                rolls.remove(dest[0])
