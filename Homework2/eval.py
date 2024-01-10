'''
from homework import open_txt, matrix_trans, matrix_further_trans
import numpy as np
'''


def heuristic_eval(board, player, opponent):
    # Get all the player pieces list
    player_list = set()
    opponent_list = set()

    for i in range(19):
        for j in range(19):
            if board[i][j] == player:
                player_list.add((i, j))
            elif board[i][j] == opponent:
                opponent_list.add((i, j))
    # print(player_list, opponent_list)
    # we get all the player pieces position, calculate can we win first.

    if can_opponent_win_all_player(board, opponent_list, player, opponent):
        return -100
    elif can_win_all_player(board, player_list, player, opponent):
        return 100
    elif can_threat_opponent_4(board, opponent_list, player, opponent):
        return -80
    elif can_defense_opponent_threat(board, player_list, opponent, player):
        return 90
    elif can_threat_player(board, player_list, player, opponent):
        return 80

    capture_points = can_capture_player(board, player_list, player, opponent)
    if capture_points:
        # value from 0 to 40, maximum capture 8 pieces per step
        return capture_points * 5

    line_points = player_line(board, player_list, player, opponent)
    if line_points:
        return line_points


def can_win(board, state, player, opponent):
    row = state[0]
    col = state[1]
    # print(state, col-4)
    if col >= 4 and ([board[row][col - i] for i in range(5)] == [player, player, player, player, player]):
        return True
    if col <= 14 and ([board[row][col + i] for i in range(5)] == [player, player, player, player, player]):
        return True
    # Check for threats in columns
    if row >= 4 and ([board[row - i][col] for i in range(5)] == [player, player, player, player, player]):
        return True
    if row <= 14 and (
            [board[row + i][col] for i in range(5)] == [player, player, player, player, player]):
        return True
    # Check for threats in diagonals (top-left to bottom-right)
    if row >= 4 and col >= 4 and (
            [board[row - i][col - i] for i in range(5)] == [player, player, player, player, player]):
        return True
    if row <= 14 and col <= 14 and (
            [board[row + i][col + i] for i in range(5)] == [player, player, player, player, player]):
        return True
    # Check for threats in diagonals (bottom-left to top-right)
    if row <= 14 and col >= 4 and (
            [board[row + i][col - i] for i in range(5)] == [player, player, player, player, player]):
        return True
    if row >= 4 and col <= 14 and (
            [board[row - i][col + i] for i in range(5)] == [player, player, player, player, player]):
        return True
    return False


def can_win_all_player(board, player_list, player, opponent):
    # checked correct
    win_state = False
    for position in player_list:
        win_state = can_win(board, position, player, opponent)
        if win_state:
            return win_state
    return win_state


def can_opponent(board, state, player):
    # player: X, opponent: O
    # Pattern: OOOOX or XOOOO
    # checked correct
    # Check for threats in rows
    row = state[0]
    col = state[1]
    if col >= 4 and [board[row][col - i] for i in range(5)] == [player, player, player, player, player]:
        return True
    if col <= 14 and [board[row][col + i] for i in range(5)] == [player, player, player, player, player]:
        return True
    # Check for threats in columns
    if row >= 4 and [board[row - i][col] for i in range(5)] == [player, player, player, player, player]:
        return True
    if row <= 14 and [board[row + i][col] for i in range(5)] == [player, player, player, player, player]:
        return True
    # Check for threats in diagonals (top-left to bottom-right)
    if row >= 4 and col >= 4 and [board[row - i][col - i] for i in range(5)] == [player, player, player, player,
                                                                                 player]:
        return True
    if row <= 14 and col <= 14 and [board[row + i][col + i] for i in range(5)] == [player, player, player, player,
                                                                                   player]:
        return True
    # Check for threats in diagonals (bottom-left to top-right)
    if row <= 14 and col >= 4 and [board[row + i][col - i] for i in range(5)] == [player, player, player, player,
                                                                                  player]:
        return True
    if row >= 4 and col <= 14 and [board[row - i][col + i] for i in range(5)] == [player, player, player, player,
                                                                                  player]:
        return True
    return False


def can_opponent_win_all_player(board, opponent_list, player, opponent):
    # player: X, opponent: O
    # Pattern: XXXXX
    win_state = False
    for position in opponent_list:
        win_state = can_opponent(board, position, opponent)
        if win_state:
            return win_state
    return win_state


def can_threat(board, state, player, opponent):
    row = state[0]
    col = state[1]

    # checked correct
    # Check for threats in rows
    if col >= 4 and ([board[row][col-i] for i in range(4)] == [player, player, player, player]) and (board[row][col-4] != opponent or board[row][col+1] != opponent):
        return True
    if col <= 14 and ([board[row][col+i] for i in range(4)] == [player, player, player, player]) and (board[row][col + 4] != opponent or board[row][col-1] != opponent):
        return True
    # Check for threats in columns
    if row >= 4 and ([board[row-i][col] for i in range(4)] == [player, player, player, player]) and (board[row-4][col] != opponent or board[row+1][col] != opponent):
        return True
    if row <= 14 and ([board[row + i][col] for i in range(4)] == [player, player, player, player]) and (board[row+4][col] != opponent or board[row-1][col] != opponent):
        return True
    # Check for threats in diagonals (top-left to bottom-right)
    if row >= 4 and col >= 4 and ([board[row - i][col - i] for i in range(4)] == [player, player, player, player]) and (board[row-4][col-4] != opponent or board[row+1][col+1] != opponent):
        return True
    if row <= 14 and col <= 14 and ([board[row + i][col + i] for i in range(4)] == [player, player, player, player]) and (board[row+4][col+4] != opponent or board[row-1][col-1] != opponent):
        return True
    # Check for threats in diagonals (bottom-left to top-right)
    if row <= 14 and col >= 4 and (
            [board[row + i][col - i] for i in range(4)] == [player, player, player, player]) and (board[row+4][col-4] != opponent or board[row-1][col+1] != opponent):
        return True
    if row >= 4 and col <= 14 and (
            [board[row - i][col + i] for i in range(4)] == [player, player, player, player]) and (board[row-4][col+4] != opponent or board[row+1][col-1] != opponent):
        return True
    return False


def can_threat_player(board, player_list, player, opponent):
    # player: X, opponent: O
    # Pattern: _XXXX or XXXX_ or OXXXX or XXXXO
    threat_state = False
    for position in player_list:
        threat_state = can_threat(board, position, player, opponent)
        if threat_state:
            # print(position, threat_state)
            return threat_state
    return threat_state


def can_threat_opponent_4(board, player_list, player, opponent):
    # player: X, opponent: O
    # Pattern: XOOOO or OOOOX
    threat_state = False
    for position in player_list:
        threat_state = can_threat(board, position, opponent, player)
        if threat_state:
            # print(position, threat_state)
            return threat_state
    return threat_state


def can_defense_threat_opponent(board, state, player, opponent):
    row = state[0]
    col = state[1]

    # checked correct
    # Check for threats in rows
    if 17 >= col >= 3 and ([board[row][col - i] for i in range(3)] == [player, player, player]) and (
            board[row][col - 3] == opponent or board[row][col + 1] == opponent):
        return True
    if 1 <= col <= 15 and ([board[row][col + i] for i in range(3)] == [player, player, player]) and (
            board[row][col + 3] == opponent or board[row][col - 1] == opponent):
        return True
    # Check for threats in columns
    if 17 >= row >= 3 and ([board[row - i][col] for i in range(3)] == [player, player, player]) and (
            board[row - 3][col] == opponent or board[row + 1][col] == opponent):
        return True
    if 1 <= row <= 15 and ([board[row + i][col] for i in range(3)] == [player, player, player]) and (
            board[row + 3][col] == opponent or board[row - 1][col] == opponent):
        return True
    # Check for threats in diagonals (top-left to bottom-right)
    if 17 >= row >= 3 and 17 >= col >= 3 and ([board[row - i][col - i] for i in range(3)] == [player, player, player]) and (
            board[row - 3][col - 3] == opponent or board[row + 1][col + 1] == opponent):
        return True
    if 1 <= row <= 15 and 1 <= col <= 15 and (
            [board[row + i][col + i] for i in range(4)] == [player, player, player]) and (
            board[row + 3][col + 3] == opponent or board[row - 1][col - 1] == opponent):
        return True
    # Check for threats in diagonals (bottom-left to top-right)
    if 1 <= row <= 15 and 17 >= col >= 3 and (
            [board[row + i][col - i] for i in range(3)] == [player, player, player]) and (
            board[row + 3][col - 3] == opponent or board[row - 1][col + 1] == opponent):
        return True
    if 17 >= row >= 3 and 1 <= col <= 15 and (
            [board[row - i][col + i] for i in range(3)] == [player, player, player]) and (
            board[row - 3][col + 3] == opponent or board[row + 1][col - 1] == opponent):
        return True
    return False


def can_defense_opponent_threat(board, player_list, player, opponent):
    # player: X, opponent: O
    # Pattern: XOOO_ or _OOOX
    threat_state = False
    for position in player_list:
        threat_state = can_defense_threat_opponent(board, position, player, opponent)
        # print(threat_state, position)
        if threat_state:
            # print(position, threat_state)
            return threat_state
    return threat_state


def can_capture(board, state, player, opponent):
    # Check if the piece at the given row and column can be captured
    row = state[0]
    col = state[1]

    capture_points = 0

    # Check horizontally
    if col >= 3 and board[row][col - 3] == player and board[row][col - 2] == opponent and board[row][
        col - 1] == opponent:
        capture_points += 1
    if col <= 15 and board[row][col + 1] == opponent and board[row][col + 2] == opponent and board[row][
        col + 3] == player:
        capture_points += 1

    # Check vertically
    if row >= 3 and board[row - 3, col] == player and board[row - 2, col] == opponent and board[row - 1][
        col] == opponent:
        capture_points += 1
    if row <= 15 and board[row + 1, col] == opponent and board[row + 2][col] == opponent and board[row + 3][
        col] == player:
        capture_points += 1

    # Check diagonally (top-left to bottom-right)
    if row >= 3 and col >= 3 and board[row - 3, col - 3] == player and board[row - 2, col - 2] == opponent and board[
        row - 1, col - 1] == opponent:
        capture_points += 1
    if row <= 15 and col <= 15 and board[row + 1, col + 1] == opponent and board[row + 2, col + 2] == opponent and \
            board[row + 3, col + 3] == player:
        capture_points += 1

    # Check diagonally (bottom-left to top-right)
    if row <= 15 and col >= 3 and board[row + 1, col - 1] == opponent and board[row + 2, col - 2] == opponent and board[
        row + 3, col - 3] == player:
        capture_points += 1
    if row >= 3 and col <= 15 and board[row - 1, col + 1] == opponent and board[row - 2][col + 2] == opponent and board[
        row - 3, col + 3] == player:
        capture_points += 1

    return capture_points


def can_capture_player(board, player_list, player, opponent):
    # player: X, opponent: O
    # Pattern: XOOX
    capture_points = 0
    for position in player_list:
        capture_points += can_capture(board, position, player, opponent)
    return capture_points


def player_line(board, player_list, player, opponent):
    # player: X, opponent: O
    # Pattern: X or XX or XXX
    line_points = 0
    best = 0
    for position in player_list:
        line_points = maximum_line_size(board, position, player, opponent)
        # print(line_points, position)
        if line_points > best:
            best = line_points
    return best


def line_calculate(board, row, col, number, player, opponent):
    line_point = 0
    if number == 3:
        if col >= number - 1 and ([board[row][col - i] for i in range(number)] == [player, player, player]):
            line_point = number
        if col <= 19 - number and ([board[row][col + i] for i in range(number)] == [player, player, player]):
            line_point = number
        # Check for threats in columns
        if row >= number - 1 and ([board[row - i][col] for i in range(number)] == [player, player, player]):
            line_point = number
        if row <= 19 - number and ([board[row + i][col] for i in range(number)] == [player, player, player]):
            line_point = number
        # Check for threats in diagonals (top-left to bottom-right)
        if row >= number - 1 and col >= number - 1 and (
                [board[row - i][col - i] for i in range(number)] == [player, player, player]):
            line_point = number
        if row <= 19 - number and col <= 19 - number and (
                [board[row + i][col + i] for i in range(number)] == [player, player, player]):
            line_point = number
        # Check for threats in diagonals (bottom-left to top-right)
        if row <= 19 - number and col >= number - 1 and (
                [board[row + i][col - i] for i in range(number)] == [player, player, player]):
            line_point = number
        if row >= number - 1 and col <= 19 - number and (
                [board[row - i][col + i] for i in range(number)] == [player, player, player]):
            line_point = number
    if number == 2:
        if col >= number - 1 and ([board[row][col - i] for i in range(number)] == [player, player]):
            line_point = number
        if col <= 19 - number and ([board[row][col + i] for i in range(number)] == [player, player]):
            line_point = number
        # Check for threats in columns
        if row >= number - 1 and ([board[row - i][col] for i in range(number)] == [player, player]):
            line_point = number
        if row <= 19 - number and ([board[row + i][col] for i in range(number)] == [player, player]):
            line_point = number
        # Check for threats in diagonals (top-left to bottom-right)
        if row >= number - 1 and col >= number - 1 and ([board[row - i][col - i] for i in range(number)] == [player, player]):
            line_point = number
        if row <= 19 - number and col <= 19 - number and (
                [board[row + i][col + i] for i in range(number)] == [player, player]):
            line_point = number
        # Check for threats in diagonals (bottom-left to top-right)
        if row <= 19 - number and col >= number - 1 and (
                [board[row + i][col - i] for i in range(number)] == [player, player]):
            line_point = number
        if row >= number - 1 and col <= 19 - number and (
                [board[row - i][col + i] for i in range(number)] == [player, player]):
            line_point = number
    return line_point


def maximum_line_size(board, state, player, opponent):
    line_point = 1
    # first consider XXX
    row = state[0]
    col = state[1]
    line_point_3 = line_calculate(board, row, col, 3, player, opponent)
    line_point = max(line_point, line_point_3)
    # consider XX, only when line_point == 0
    if line_point == 1:
        line_point_2 = line_calculate(board, row, col, 2, player, opponent)
        # print(f'This is the line_2', line_point_2)
        line_point = max(line_point, line_point_2)
    '''
    # maybe not need X
    if line_point == 0:
        line_point = line_calculate(board, row, col, 1, player, opponent)
    '''
    return line_point


'''
if __name__ == '__main__':
    t_matrix = open_txt('./input2.txt')
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
    print(f'This is who first', character)

    # Get the total time for the game
    game_time = float(t_matrix[1][0])
    print(f'This is the total game time:', game_time)

    # Get the captured pieces by white and black
    before_transfer_captured = t_matrix[2][0]
    captured = matrix_further_trans(t_matrix[2][0])
    white_captured = int(captured[0])
    black_captured = int(captured[1])
    print(f'This is the captured information:', white_captured, black_captured)

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

    print(board_table)
    # value = can_threat(board_table, (10, 9), character)
    value = heuristic_eval(board_table, character, opponent)
    print(value)
'''