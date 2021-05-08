import utils

board = utils.getBoard()

s1, s2 = utils.toIndex("l1 e1")
res = utils.move(board, s1, 6, "y")
utils.printTable(board)


s1, s2 = utils.toIndex("e1 e1")
res = utils.move(board, s1, 1, "x")
utils.printTable(board)
