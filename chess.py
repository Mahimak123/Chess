#step 1: board
#step 2: pieces
#step 3: turns
#step 4: move pieces on each turn

#check if move is valid
#checkmate and condition
#castling and in passant

board = [0] * 8

for i in range(len(board)):
    board[i] = ["  "] * 8

#[8 x 8]
#(0, 0) -> a8 
def print_board(board):
    for i, row in enumerate(board):
        print(8 - i, end = ": ")
        for j, col in enumerate(row):
            print(col, end = " ")
        print("\n") 
    print(" " * 3 + "a" + " " * 2 + "b" + " " * 2 + "c" + " " * 2 + "d" + " " * 2 + "e" + " " * 2 + "f" + " " * 2 + "g" + " " * 2 + "h" ) 

white_pieces_map = {
    "wP": [(6,0), (6,1), (6,2), (6,3), (6,4), (6,5), (6,6), (6,7)],
    "wN": [(7,1), (7,6)],
    "wB": [(7,2), (7,5)],
    "wR": [(7,0), (7,7)],
    "wQ": [(7,3)],
    "wK": [(7,4)]
}

black_pieces_map = {
    "bP": [(1,0), (1,1), (1,2), (1,3), (1,4), (1,5), (1,6), (1,7)],
    "bN": [(0,1), (0,6)],
    "bB": [(0,2), (0,5)],
    "bR": [(0,0), (0,7)],
    "bQ": [(0,3)],
    "bK": [(0,4)]
}

col_map = {
     "a": 0,
     "b": 1,
     "c": 2,
     "d": 3,
     "e": 4,
     "f": 5,
     "g": 6,
     "h": 7
}

def put_pieces(board):
    #white pieces
    for piece, squares in white_pieces_map.items():
        for square in squares:
             x, y = square[0], square[1]
             board[x][y] = piece

    #black pieces
    for piece, squares in black_pieces_map.items():
        for square in squares:
            x, y = square[0], square[1]
            board[x][y] = piece

put_pieces(board)


curr_turn = 1

while(True):
    print_board(board)
    print("") 

    curr_player = ""
    if curr_turn % 2 == 1:
        curr_player = "white"
    else:
        curr_player = "black"

    curr_turn += 1

    print(curr_player + " to move!")
    print("")

    starting_square = input("Enter the square whose piece you'd like to play: ")
    start_x, start_y = starting_square[0], starting_square[1]
    start_x =  col_map[start_x]
    start_y = 8 - int(start_y)
    start_x, start_y = start_y, start_x

    ending_square = input("Enter the square whose piece you'd like to move your piece to: ")
    end_x, end_y = ending_square[0], ending_square[1]
    end_x =  col_map[end_x]
    end_y = 8 - int(end_y)
    end_x, end_y = end_y, end_x

    temp = board[start_x][start_y]
    board[start_x][start_y] = " "
    board[end_x][end_y] =  temp

    # Validate move
def is_valid_move(start_x, start_y, end_x, end_y, player):
    piece = board[start_x][start_y]
    if piece == " " or (player == "white" and piece[0] != "w") or (player == "black" and piece[0] != "b"):
        return False
    target = board[end_x][end_y]
    if target != " " and target[0] == piece[0]:
        return False
    return True  # Basic validation (expand for piece-specific rules)

# Checkmate detection
def is_checkmate(player):
    king = "wK" if player == "white" else "bK"
    for i in range(8):
        for j in range(8):
            if board[i][j] == king:
                return False  # King is still on board
    return True  # King is missing (checkmate)

# Castling
def can_castle(player, side):
    row = 7 if player == "white" else 0
    king, rook = "wK" if player == "white" else "bK", "wR" if player == "white" else "bR"
    if board[row][4] != king:
        return False
    if side == "kingside" and board[row][7] == rook and board[row][5] == " " and board[row][6] == " ":
        return True
    if side == "queenside" and board[row][0] == rook and board[row][1:4] == [" "] * 3:
        return True
    return False

def perform_castling(player, side):
    row = 7 if player == "white" else 0
    if side == "kingside":
        board[row][4], board[row][6] = " ", "wK" if player == "white" else "bK"
        board[row][7], board[row][5] = " ", "wR" if player == "white" else "bR"
    else:
        board[row][4], board[row][2] = " ", "wK" if player == "white" else "bK"
        board[row][0], board[row][3] = " ", "wR" if player == "white" else "bR"

# En passant
def is_en_passant(start_x, start_y, end_x, end_y, player):
    if board[start_x][start_y][1] != "P":
        return False
    direction = -1 if player == "white" else 1
    if abs(end_y - start_y) == 1 and end_x == start_x + direction:
        if board[start_x][end_y][1] == "P" and board[start_x][end_y][0] != board[start_x][start_y][0]:
            return True
    return False

def perform_en_passant(start_x, start_y, end_x, end_y):
    board[start_x][end_y] = " "
    board[end_x][end_y] = board[start_x][start_y]
    board[start_x][start_y] = " "

# Game loop continuation
while True:
    print_board()
    player = "white" if curr_turn % 2 == 1 else "black"
    print(f"{player} to move!")

    start = input("Enter piece position (e.g., e2): ")
    end = input("Enter destination (e.g., e4): ")

    start_x, start_y = 8 - int(start[1]), col_map[start[0]]
    end_x, end_y = 8 - int(end[1]), col_map[end[0]]

    if is_valid_move(start_x, start_y, end_x, end_y, player):
        if is_en_passant(start_x, start_y, end_x, end_y, player):
            perform_en_passant(start_x, start_y, end_x, end_y)
        else:
            board[end_x][end_y], board[start_x][start_y] = board[start_x][start_y], " "

        if is_checkmate(player):
            print(f"{player} is in checkmate! Game over.")
            break

        curr_turn += 1
    else:
        print("Invalid move! Try again.")
