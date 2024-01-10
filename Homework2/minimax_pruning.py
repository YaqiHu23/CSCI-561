import math
from eval import heuristic_eval


def normal_position_detect(board, position_x, position_y):
    # checked correct
    for r, c in ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)):
        x, y = position_x + r, position_y + c
        if 0 <= x <= 18 and 0 <= y <= 18:
            if board[x][y] == 'w' or board[x][y] == 'b':
                return True
    return False


def next_move(board, player, opponent):
    # checked correct
    # check 3 levels from the point.
    moves = set()
    for row in range(19):
        for col in range(19):
            if board[row][col] == player or board[row][col] == opponent:
                # print(f'detected', (row, col))
                # print('-----------------------')
                for r1, c1 in ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)):
                    x, y = row + r1, col + c1
                    if 0 <= x <= 18 and 0 <= y <= 18:
                        if board[x][y] == '.':
                            # print((x, y), normal_position_detect(board, x, y))
                            if normal_position_detect(board, x, y):
                                # print(f'This is first level', (x, y))
                                moves.add((x, y))
                # print(moves)
                for r2, c2 in ((-2, -2), (-2, 0), (-2, 2), (0, -2), (0, 2), (2, -2), (2, 0), (2, 2)):
                    x2, y2 = row + r2, col + c2
                    if 0 <= x2 <= 18 and 0 <= y2 <= 18:
                        if board[x2][y2] == '.':
                            if normal_position_detect(board, x2, y2):
                                # print(f'This is second level', (x2, y2))
                                moves.add((x2, y2))
                for r3, c3 in ((-3, -3), (-3, 0), (-3, 3), (0, -3), (0, 3), (3, -3), (3, 0), (3, 3)):
                    x3, y3 = row + r2, col + c2
                    if 0 <= x3 <= 18 and 0 <= y3 <= 18:
                        if board[x3][y3] == '.':
                            if normal_position_detect(board, x3, y3):
                                # print(f'This is third level', (x3, y3))
                                moves.add((x3, y3))

    return moves


def get_captured_position(board, dx, dy, player, opponent):
    # checked correct
    next_captured = []
    for r, c in ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)):
        # move one step
        x, y = dx + r, dy + c
        x2, y2 = x + r, y + c
        x3, y3 = x2 + r, y2 + c
        if 0 <= x <= 18 and 0 <= y <= 18 and 0 <= x3 <= 18 and 0 <= y3 <= 18 and 0 <= x2 <= 18 and 0 <= y2 <= 18 and \
                board[x][y] == opponent and board[x2][y2] == opponent and board[x3][y3] == player:
            next_captured.append((x, y))
            next_captured.append((x2, y2))

    return next_captured


def implement_move(board, move_im, player):
    # checked correct
    positionx = move_im[0]
    positiony = move_im[1]
    new_board = board.copy()
    new_board[positionx][positiony] = player
    return new_board


def eat_capture(eat_board, move_eat, player_eat, opponent_eat, white_captured_eat, black_captured_eat):
    # find if we captured any
    positionx = move_eat[0]
    positiony = move_eat[1]
    next_captured = get_captured_position(eat_board, positionx, positiony, player_eat, opponent_eat)
    # we will return a list of captured
    if next_captured:
        # Replace the opponent's captured pieces with empty spaces
        for x, y in next_captured:
            eat_board[x][y] = "."
            if player_eat == 'w':
                white_captured_eat += 1
            elif player_eat == 'b':
                black_captured_eat += 1
    return [eat_board, white_captured_eat, black_captured_eat]


def minimax(board, depth, alpha, beta, player_mini, opponent_mini, white_captured_mini, black_captured_mini, move_list):
    [value, position] = max_value(board, depth, alpha, beta, player_mini, opponent_mini, white_captured_mini, black_captured_mini, move_list)
    # print(value, position)
    return [value, position]


def max_value(board, depth, alpha, beta, player_max, opponent_max, white_captured_max, black_captured_max, move_list):
    if depth == 0:  # or is_over(board, white_captured, black_captured):
        return heuristic_eval(board, player_max, opponent_max), (0, 0)

    best_score = -math.inf
    # max our win possibility
    next_move_m = (0, 0)
    for move_max in move_list:
        # print(f'This is the best score and depth', best_score, depth)
        new_board = implement_move(board, move_max, player_max)
        # print(new_board)
        # print(new_board)
        min_move_list = move_list.copy()
        # print(move_max, min_move_list)
        min_move_list.discard(move_max)
        temp_value = min_value(new_board, depth - 1, alpha, beta, opponent_max, player_max, white_captured_max,
                               black_captured_max, min_move_list)
        # print(move_list)
        # print(temp_value, move_max)
        # print(move_max, temp_value)
        if best_score < temp_value:
            best_score = temp_value
            next_move_m = move_max
            # print('This is the next move', next_move_m, best_score)
        # print(best_score, next_move_m)
        if best_score >= beta:
            return best_score, next_move_m

        alpha = max(alpha, best_score)
    return best_score, next_move_m


def min_value(board, depth, alpha, beta, player_min, opponent_min, white_captured_min, black_captured_min, move_list):
    if depth == 0:
        return heuristic_eval(board, opponent_min, player_min)

    best_score = math.inf
    for move_min in move_list:
        # print(f'This this the list for min', move)
        new_board = implement_move(board, move_min, player_min)
        # print(f'This is the min move', move_min)
        max_move_list = move_list.copy()
        max_move_list.discard(move_min)
        temp_value, next_move_min = max_value(new_board, depth - 1, alpha, beta, opponent_min, player_min, white_captured_min, black_captured_min, max_move_list)
        # print(f'This is the temp_value and depth', temp_value, depth)
        if best_score > temp_value:
            best_score = temp_value

        if best_score <= alpha:
            return best_score

        beta = min(beta, best_score)
    return best_score

'''
if __name__ == '__main__':
    t_matrix = open_txt('./input.txt')
    t_matrix = matrix_trans(t_matrix)
    # print(t_matrix)

    # Get each part from txt
    # Get which one first, black or white
    character = str(t_matrix[0][0])
    if character == 'BLACK':
        character = 'b'
        opponent = 'w'
    elif character == 'WHITE':
        character = 'w'
        opponent = 'b'
    # print(f'This is who first and opponent', character, opponent)

    # Get the total time for the game
    game_time = float(t_matrix[1][0])
    # print(f'This is the total game time:', game_time)

    # Get the captured pieces by white and black
    before_transfer_captured = t_matrix[2][0]
    captured = matrix_further_trans(t_matrix[2][0])
    white_captured = int(captured[0])
    black_captured = int(captured[1])
    # print(f'This is the captured information:', white_captured, black_captured)

    # Get the txt table, and transfer it to a matrix
    board_table = np.zeros((19, 19), str)
    for i in range(0, 19):
        txt_table = t_matrix[i + 3]  # each row of txt matrix
        txt_table = str(txt_table[0])
        for j in range(0, 19):
            if txt_table[j] == '.':
                board_table[i][j] = '.'
            elif txt_table[j] == 'w':
                board_table[i][j] = 'w'
            elif txt_table[j] == 'b':
                board_table[i][j] = 'b'
    # board_table[10][9] = 'w'
    # board_table[10][10] = 'b'
    # board_table[10][11] = 'b'
    # print(board_table)

    main_board = board_table.copy()

    start = time.perf_counter()
    current = -math.inf
    
    moves = next_move(board_table, character, opponent)
    for position in moves:
        # print(position)
        new_moves = moves.copy()
        new_moves.discard(position)
        # print(new_moves)
        main_board = board_table.copy()

        # main_new_board = implement_move(main_board, position, character)
        bestc = minimax(main_board, 1, -math.inf, math.inf, character, opponent, white_captured, black_captured, new_moves)
        print(position, bestc)
        # bestc = -bestc
        # print(bestc, position)

        if bestc > current:
            current = bestc
            # next_move_p contains the position we need to implement finally
            next_move_p = position

    moves = next_move(board_table, character, opponent)
    [bestc, next_move_p] = minimax(main_board, 6, -math.inf, math.inf, character, opponent, white_captured, black_captured, moves)

    # print(bestc, next_move_p)
    final_board = implement_move(board_table, next_move_p, character)
    [final_board, white_captured_move, black_captured_move] = eat_capture(final_board, next_move_p, character, opponent,
                                                                          white_captured, black_captured)
    white_captured += white_captured_move
    black_captured += black_captured_move
    end = time.perf_counter()
    print(next_move_p)
    print(final_board)
    print(end - start)
    write_txt(next_move_p)
    # print(bestc, next_move_p, end - start)
'''

