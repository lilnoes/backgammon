import utils

board = utils.getBoard()
print(board["data"][6:12])

for i in range(3):
    print(i)
else:
    print("nah")

# while True:
#     print("Rolling...")
#     rolls = utils.rollDice()
#     print(f"Rolled {rolls[0]} and {rolls[1]}")
#     rolls = rolls + rolls if rolls[0] == rolls[1] else rolls
#     while len(rolls) != 0:
#         sources = input(f"dice = {rolls[-1]}, Please enter source :")
#         s1 = utils._toIndex(sources)
#         rolls.pop()
