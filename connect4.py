from connect4_AI import draw_board
import numpy as np

ROW_COUNT = 4
COLUMN_COUNT = 4

DRAW_COUNT = [[0, 0, 0, 0,]
              [0, 0, 0, 0,]
              [0, 0, 0, 0,]
              [0, 0, 0, 0,]]
def create_board():
  board = np.zeros((ROW_COUNT,COLUMN_COUNT))
  return board

def drop_piece(board, row, col, piece):
  board[row][col] = piece

def is_valid_location(board, col):
  return board[ROW_COUNT - 1][col] == 0

def get_next_open_row(board, col):
  for r in range(ROW_COUNT):
    if board[r][col] == 0:
      return r

def print_board(board):
  print(np.flip(board, 0))

def winning_move(board, piece):
  #Check horizontal location for win
  for c in range(COLUMN_COUNT-1): #4-1
    for r in range(ROW_COUNT):
        if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
          return True
  
  #Check vertical location for win
  for c in range(COLUMN_COUNT):
    for r in range(ROW_COUNT-1): #4-1
        if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
          return True

  #Check positively sloped diaganols
    for c in range(COLUMN_COUNT-1):
      for r in range(ROW_COUNT-1):
          if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
            return True
  #Check negatively sloped diaganols
    for c in range(COLUMN_COUNT-1):
      for r in range(3, ROW_COUNT):
          if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
            return True
draw = 0
def check_draw(board):  
  for i in range(ROW_COUNT):
    for j in range(COLUMN_COUNT):
      if board[i][j] == DRAW_COUNT[i][j] :
        draw = 1      
board = create_board()
print_board(board)

game_over = False
turn = 0

while not game_over:
  if turn == 0:
    col = int(input("Player 1: make your selection (0-2):"))

    if is_valid_location(board, col):
      row = get_next_open_row(board, col)
      drop_piece(board, row, col, 1)
      if winning_move(board, 1):
        print("PLAYER 1 Wins!")
        game_over = True

  #Ask for player 2 input
  else:
     col = int(input("Player 2: make your selection (0-2):"))

     if is_valid_location(board, col):
      row = get_next_open_row(board, col)
      drop_piece(board, row, col, 2)

      if winning_move(board, 2):
        print("PLAYER 2 Wins!")
        game_over = True

  print_board(board)

  turn += 1
  turn = turn % 2