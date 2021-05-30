import utils

print("Backgammon game\n\n\n")

choice = input("Load an existing game? (y for yes, n for no) :")

if(choice.lower() == 'y'):
    board = utils.restore()
    player = board['data'][2][8]['str']
    player = "x" if player == "y" else "y"

else:
    board = utils.getBoard()
    while True:
        rolls = utils.rollDice()
        utils.updateLog(str(rolls[0]))
        utils.updateLog(str(rolls[1]))
        if rolls[0] == rolls[1]:
            continue
        if rolls[0] > rolls[1]:
            print("\n\nFirst player will be x")
            player = "y" #First player will be x
        else:
            print("\n\nSecond player will be y")
            player = "x"
        break

while True:
    utils.clear()
    utils.updateTable(board)
    if board["x"] == 0:
        print("X won")
        break
    elif board["y"] == 0:
        print("Y won")
        break
    player = "y" if player == "x" else "x"
    board['data'][2][8]['str'] = player
    playerstr = "Player 1" if player == "x" else "Player 2"

    print(f"{playerstr} turn")
    utils.printTable(board)

    choice = input("Save game? (y for yes, n for no) :")
    utils.save(board)
    if choice.lower() == "y":
        break

    print("Rolling...")
    rolls = utils.rollDice()
    utils.updateLog(f"{player} {rolls[0]} {rolls[1]}")

    board["data"][2][5]["str"] = str(rolls[0])
    board["data"][2][6]["str"] = str(rolls[1])

    print(f"{player} turn")
    print(f"Rolled {rolls[0]} and {rolls[1]}")
    rolls = (rolls + rolls) if rolls[0] == rolls[1] else rolls

    while len(rolls) != 0:
        print("rolls", rolls)
        utils.printTable(board)
        if utils.flanksVar(board, player):
            if not utils.canFlankBeMoved(board, rolls, player):
                print("Can not be moved, going to next player")
                break
            utils.moveFlank(board, rolls, player)
            continue
        if not utils.movesVar(board, rolls, player):
            print("No moves available, next player")
            break

        playerstr = "Player 1" if player == "x" else "Player 2"
        source = input(f"({playerstr}) Please choose source: ")
        dest = utils.parse(source)
        if dest[0] not in rolls:
            print(f"{dest[0]} not in rolled numbers")
        elif utils.move(board, source, player):
            rolls.remove(dest[0])
        else:
            print("Try again, you can do it")
