import numpy as np
import random
import pygame
import sys
import math

#our written code have many sections
#//////////////////////////////////////
#our code starts here

BLUE = (48, 71, 94)
BLACK = (58, 64, 68)
RED = (255, 0, 0)
YELLOW = (255, 248, 28)
WHITE = (255,255,255)

ROW_COUNT = 6
COLUMN_COUNT = 7

PLAYER = 0
AI = 1

EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2

#Section 1

#this DRAW_COUNT we made for the draw condition
DRAW_COUNT = [[0, 0, 0, 0, 0, 0, 0,],
              [0, 0, 0, 0, 0, 0, 0,],
              [0, 0, 0, 0, 0, 0, 0,],
              [0, 0, 0, 0, 0, 0, 0,],
              [0, 0, 0, 0, 0, 0, 0,],
              [0, 0, 0, 0, 0, 0, 0,],]
#our code end here
#//////////////////////////////////////

WINDOW_LENGTH = 4


def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0


def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r


def print_board(board):
    print(np.flip(board, 0))


def winning_move(board, piece):
    # Check for horizontal winning if the pieces connected for 4 row pieces.
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # Check for vertical winning if the pieces connected for 4 column pieces
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # Check for vertical winning if the pieces connected for 4 positive diagonal pieces
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # Check for vertical winning if the pieces connected for 4 negative diagonal pieces
    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True


def evaluate_window(window, piece):
    score = 0
    opp_piece = PLAYER_PIECE
    if piece == PLAYER_PIECE:
        opp_piece = AI_PIECE

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2

    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 4

    return score


def score_position(board, piece):
    score = 0

    # Score center column
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    # Score Horizontal
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COLUMN_COUNT-3):
            window = row_array[c:c+WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Score Vertical
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROW_COUNT-3):
            window = col_array[r:r+WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Score posiive sloped diagonal
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score


def is_terminal_node(board):
    return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0

#//////////////////////////////////////
#Section 2
#our code starts here
def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return (None, 100000000000000)
            elif winning_move(board, PLAYER_PIECE):
                return (None, -10000000000000)
            else:  #When game is over, there will be no more valid moves
                return (None, 0)
        else:  #Depth is zero
            return (None, score_position(board, AI_PIECE))
    if maximizingPlayer: #Maximizing player
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE)
            new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else:  #Minimizing player
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value
    #our code ends here
    #//////////////////////////////////////


def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations


def pick_best_move(board, piece):

    valid_locations = get_valid_locations(board)
    best_score = -10000
    best_col = random.choice(valid_locations)
    for col in valid_locations:
        row = get_next_open_row(board, col)
        temp_board = board.copy()
        drop_piece(temp_board, row, col, piece)
        score = score_position(temp_board, piece)
        if score > best_score:
            best_score = score
            best_col = col

    return best_col


def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r *
                                            SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(
                c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == PLAYER_PIECE:
                pygame.draw.circle(screen, RED, (int(
                    c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == AI_PIECE:
                pygame.draw.circle(screen, YELLOW, (int(
                    c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
    pygame.display.update()

#//////////////////////////////////////
#Section 3
#this function we made will check the draw condition if the player places all pieces to the board


def check_draw(board):
    for i in range(ROW_COUNT):
        for j in range(COLUMN_COUNT):
            if board[3][j] != DRAW_COUNT[3][j]:
                return True
#our code ends here
#//////////////////////////////////////

board = create_board()
print_board(board)
game_over = False

pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("mvboli", 75)

turn = PLAYER #we make the first turn to be the player in every turn


while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == PLAYER:
                pygame.draw.circle(
                    screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)

        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            if turn == PLAYER:
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARESIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, PLAYER_PIECE)

                    if winning_move(board, PLAYER_PIECE):
                        label = myfont.render("Player Wins!!", 1, RED)
                        screen.blit(label, (120, 0.5))
                        game_over = True
                    #//////////////////////////////////////
                    #Section 4
                    #Draw condtion working section
                    # this is our code that the draw condition will work.
                    if not game_over:
                        for c in range(COLUMN_COUNT-6):
                            for r in range(ROW_COUNT):
                                if  r == 5 and board[5][c] != 0 and board[5][c+1] != 0 and board[5][c+2] != 0 and board[5][c+3] != 0 and board[5][c+4] != 0 and board[5][c+5] != 0 and board[5][c+6] != 0:
                                    if check_draw(board):
                                        label = myfont.render(
                                            "DRAW!!", 1, WHITE)
                                        screen.blit(label, (170, 10))
                                        print("Draw!")
                                        game_over = True
                    # this is the end of our code
                    #//////////////////////////////////////

                    turn += 1
                    turn = turn % 2

                    print_board(board)
                    draw_board(board)

    if turn == AI and not game_over:

        col, minimax_score = minimax(board, 5, -math.inf, math.inf, True) 
        # this is the ply we used which is 5 at the second parameter (depth parameter)

        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, AI_PIECE)

            if winning_move(board, AI_PIECE):
                label = myfont.render("AI Wins!!", 1, YELLOW)
                screen.blit(label, (170, 10))
                game_over = True
            #//////////////////////////////////////
            #Section 5
            #Draw condtion working section 
            # this is our code that the draw condition will work.
            if not game_over:
                for c in range(COLUMN_COUNT-6):
                    for r in range(ROW_COUNT):
                        if r == 5 and board[5][c] != 0 and board[5][c+1] != 0 and board[5][c+2] != 0 and board[5][c+3] != 0 and board[5][c+4] != 0 and board[5][c+5] != 0 and board[5][c+6] != 0:
                            if check_draw(board):
                                label = myfont.render("DRAW!!", 2, WHITE)
                                screen.blit(label, (170, 10))
                                print("Draw!")
                                game_over = True
            # this is the end of our code
            #//////////////////////////////////////

            print_board(board)
            draw_board(board)

            turn += 1
            turn = turn % 2

    if game_over:
        pygame.time.wait(3000)
