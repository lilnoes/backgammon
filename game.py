import utils

print(utils.getDest(0, 0, 1, "y"))

board = utils.getBoard()
utils.printTable(board)
utils.move(board, "2a5", "x"), utils.printTable(board)
utils.move(board, "2l1", "y"), utils.printTable(board)
utils.move(board, "6j1", "y"), utils.printTable(board)
utils.printTable(board)
typea = "x"

while True:
    typea = "y" if typea == "x" else "x"
    print("Rolling...")
    # rolls = utils.rollDice()
    rolls = [1,1]
    board["data"][2][5]["str"] = str(rolls[0])
    board["data"][2][6]["str"] = str(rolls[1])
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
            source = input("Please choose source: ")
            dest = utils.parse(source)
            if not utils.move(board, source, typea):
                print("TRy again, you can do it")
            else:
                rolls.remove(dest[0])
