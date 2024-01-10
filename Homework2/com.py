from homework import open_txt
from homework import matrix_trans
from homework import matrix_further_trans
import numpy as np
import os

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
print(board_table)
positionx_array = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T']

# board_table[8][6] = '.'
# board_table[9][6] = '.'
board_table[9][10] = 'w'
board_table[11][4] = 'b'
time = str(110)

if os.path.isfile('input2.txt'):
    os.remove('input2.txt')
txt_name = 'input2.txt'

with open(txt_name, 'a') as file:
    file.write('WHITE')
    file.write('\n')
    file.write(time)
    file.write('\n')
    output1 = str(white_captured) + ',' + str(black_captured)
    file.write(output1)
    file.write('\n')
    for i in range(19):
        output = str()
        for j in range(19):
            output = output + str(board_table[i][j])
        file.write(output)
        file.write('\n')
