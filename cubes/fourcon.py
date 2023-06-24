

def make_move(player, column, board):
    counter = len(board) - 1
    placed = False
    strGenerator = ""
    while not placed:
        if board[counter][column] == "*":
            s = board[counter]
            strGenerator = s[:column] + player + s[column + 1:]
            placed = True
        if counter < 0:
            print("Invalid")
            return
        counter -= 1
    board[counter + 1] = strGenerator


def draw_board(board):
    for row in board:
        for item in row:
            print(" " + item + " ", end="")
        print()


board = ["*******", "*******", "XO*****", "OX*****", "XO*****", "OX*****"]
print("Before:")
draw_board(board)
print()
make_move("X", 1, board)
print("After:")
draw_board(board)
