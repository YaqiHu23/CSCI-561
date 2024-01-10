import os
import numpy as np
import re
from minimax_pruning import minimax
from minimax_pruning import next_move
from minimax_pruning import eat_capture
from minimax_pruning import implement_move
import time
import math


def empty_board(main_board):
    for i in range(19):
        for j in range(19):
            if main_board[i][j] != '.':
                return False
    return True


def only_one_player(main_board, player):
    count = 0
    for i in range(19):
        for j in range(19):
            if main_board[i][j] == player:
                count += 1
    return count


def call_minimax(main_board, depth, character, opponent, white_captured, black_captured):
    moves = next_move(board_table, character, opponent)
    moves_count = len(moves)
    # print(moves_count)
    if depth != 1:
        [bestc_1, next_move_p_1] = minimax(main_board, 1, -math.inf, math.inf, character, opponent, white_captured,
                                       black_captured, moves)
        # print(f'This is depth1 best', bestc_1)
        if bestc_1 == 100:
            next_move_p = next_move_p_1
        elif bestc_1 == 80:
            next_move_p = next_move_p_1
        elif bestc_1 == 90:
            next_move_p =next_move_p_1
        else:
            if depth == 4:
                if moves_count >= 50:
                    [bestc, next_move_p_d] = minimax(main_board, 2, -math.inf, math.inf, character, opponent, white_captured,
                                   black_captured, moves)
                    next_move_p = next_move_p_d
                elif 30 <= moves_count < 50:
                    [bestc, next_move_p_d] = minimax(main_board, 3, -math.inf, math.inf, character, opponent,
                                                     white_captured,
                                                     black_captured, moves)
                    next_move_p = next_move_p_d
                else:

                    [bestc, next_move_p_d] = minimax(main_board, depth, -math.inf, math.inf, character, opponent,
                                                     white_captured,
                                                     black_captured, moves)
                    next_move_p = next_move_p_d
            elif depth == 3:
                if moves_count >= 35:
                    [bestc, next_move_p_d] = minimax(main_board, 2, -math.inf, math.inf, character, opponent,
                                                     white_captured,
                                                     black_captured, moves)
                    next_move_p = next_move_p_d
                else:
                    [bestc, next_move_p_d] = minimax(main_board, depth, -math.inf, math.inf, character, opponent,
                                                     white_captured,
                                                     black_captured, moves)
                    next_move_p = next_move_p_d
    else:
        [bestc, next_move_p] = minimax(main_board, depth, -math.inf, math.inf, character, opponent, white_captured,
                                         black_captured, moves)
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


def open_txt(path):
    with open(path, encoding='utf-8') as file:
        matrix = file.read()
        matrix = matrix.rstrip()
    return matrix


def write_txt(position):
    positionx_array = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T']
    output_position_x = 19 - position[0]
    output_position_y = positionx_array[position[1]]
    output = str(output_position_x) + str(output_position_y)
    if os.path.isfile('output.txt'):
        os.remove('output.txt')
    txt_name = 'output.txt'

    with open(txt_name, 'a') as file:
        file.write(output)


def matrix_trans(matrix):
    rows = matrix.splitlines()
    temp_matrix = [row.split('\n') for row in rows if row.strip()]
    return np.array(temp_matrix)


def matrix_further_trans(matrix):
    rows = matrix
    temp_matrix = re.findall(r"\d+\.?\d*", rows)
    return np.ravel(temp_matrix)


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
    # print(f'This is who first', character)

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

    # What function we need?
    # decide next move function: next_move()
    # minmax function: minmax()
    # alpha-beta pruning function: alpha_beta()
    # heuristic_eval function: heuristic_eval()
    # name maybe different.

    main_board = board_table.copy()
    start = time.perf_counter()
    current = -math.inf
    # print(main_board)
    calibrate_time = open_txt('./calibrate.txt')
    cpu_time = int(calibrate_time)
    depth = 1
    # print(cpu_time, game_time)
    if cpu_time <= 100:
        if game_time > 100.0:
            depth = 4
            if character == 'w' and empty_board(main_board):
                write_txt((9, 9))
            elif character == 'w' and only_one_player(main_board, 'w') == 1:
                if board_table[9][6] == '.':
                    write_txt((9, 6))
                else:
                    write_txt((9, 12))
            else:
                call_minimax(main_board, depth, character, opponent, white_captured, black_captured)
        elif 30.0 < game_time <= 100.0:
            depth = 3
            if character == 'w' and empty_board(main_board):
                write_txt((9, 9))
            elif character == 'w' and only_one_player(main_board, 'w') == 1:
                if board_table[9][6] == '.':
                    write_txt((9, 6))
                else:
                    write_txt((9, 12))
            else:
                call_minimax(main_board, depth, character, opponent, white_captured, black_captured)
        elif 10.0 < game_time <= 30.0:
            depth = 2
            if character == 'w' and empty_board(main_board):
                write_txt((9, 9))
            elif character == 'w' and only_one_player(main_board, 'w') == 1:
                if board_table[9][6] == '.':
                    write_txt((9, 6))
                else:
                    write_txt((9, 12))
            else:
                call_minimax(main_board, depth, character, opponent, white_captured, black_captured)
        else:
            depth = 1
            # print(depth)
            if character == 'w' and empty_board(main_board):
                write_txt((9, 9))
            elif character == 'w' and only_one_player(main_board, 'w') == 1:
                if board_table[9][6] == '.':
                    write_txt((9, 6))
                else:
                    write_txt((9, 12))
            else:
                call_minimax(main_board, depth, character, opponent, white_captured, black_captured)

    elif cpu_time > 100:
        if game_time > 150.0:
            depth = 4
            if character == 'w' and empty_board(main_board):
                write_txt((9, 9))
            elif character == 'w' and only_one_player(main_board, 'w') == 1:
                if board_table[9][6] == '.':
                    write_txt((9, 6))
                else:
                    write_txt((9, 12))
            else:
                call_minimax(main_board, depth, character, opponent, white_captured, black_captured)
        elif 60.0 < game_time <= 150.0:
            depth = 3
            if character == 'w' and empty_board(main_board):
                write_txt((9, 9))
            elif character == 'w' and only_one_player(main_board, 'w') == 1:
                if board_table[9][6] == '.':
                    write_txt((9, 6))
                else:
                    write_txt((9, 12))
            else:
                call_minimax(main_board, depth, character, opponent, white_captured, black_captured)
        elif 30.0 < game_time <= 60.0:
            depth = 2
            if character == 'w' and empty_board(main_board):
                write_txt((9, 9))
            elif character == 'w' and only_one_player(main_board, 'w') == 1:
                if board_table[9][6] == '.':
                    write_txt((9, 6))
                else:
                    write_txt((9, 12))
            else:
                call_minimax(main_board, depth, character, opponent, white_captured, black_captured)
        else:
            depth = 1
            if character == 'w' and empty_board(main_board):
                write_txt((9, 9))
            elif character == 'w' and only_one_player(main_board, 'w') == 1:
                if board_table[9][6] == '.':
                    write_txt((9, 6))
                else:
                    write_txt((9, 12))
            else:
                call_minimax(main_board, depth, character, opponent, white_captured, black_captured)