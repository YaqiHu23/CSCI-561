from utility import open_txt, matrix_trans, write_txt, print_KB, nagated_Query, fresh_KB, change_KB_facts_p, sort_KB
from deal_input import re_triving_noninfer
from trans_CNF import extract_sentences, trans_CNF
from resolution import resolution_function
import time


run_time = time.time()
KB_sentence = []
KB = []
final_state = False

t_matrix = open_txt('./Examples/hw3_10_examples/test_case_4/input.txt')
# t_matrix = open_txt('./input.txt')
t_matrix = matrix_trans(t_matrix)

Query = re_triving_noninfer(t_matrix[0][0])
Query, state = trans_CNF(Query)
# print(Query[0])
Query = nagated_Query(Query[0])
Query[0] = []
# print(f'This is the Query\n', Query)

KB_size = int(t_matrix[1])
for i in range(2, KB_size + 2):
    KB.append(t_matrix[i][0])
# print(f'This is the KB')
# print_KB(KB)
KB = extract_sentences(KB)
# print('This is transferred CNF KB')
# print_KB(KB)
# CNF transfer finished, all in CNF now

# Next we fresh KB to some [[], [[1], [2],...]]
# [] is for unification space

KB = fresh_KB(KB)
KB = change_KB_facts_p(KB)
KB.insert(0, Query)
KB = sort_KB(KB)

# print_KB(KB)
final_state = resolution_function(KB, run_time)
# print('\n')
# print(final_state)
# After resolution, we get the answer.
# Write answer to output.txt
write_txt(final_state)