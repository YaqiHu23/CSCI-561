import copy
import os
import numpy as np
import re


def delete_multi(sentence):
    # Checked corrected
    new_sentence = copy.deepcopy(sentence)
    compare_set = []
    delete_list = []
    # Format: [ [[x,Name], [y, Name]], [[Predicate1, vars], [Predicate2, vars], ...] ]
    for i in range(len(new_sentence[1])):
        # Format: [[Predicate1, vars], [Predicate2, vars], ...]
        if new_sentence[1][i] != '|':
            if new_sentence[1][i] in compare_set:
                if i == len(new_sentence[1]) - 1:
                    if i - 1 not in delete_list:
                        delete_list.append(i - 1)
                    delete_list.append(i)
                else:
                    delete_list.append(i)
                    if i + 1 not in delete_list:
                        delete_list.append(i + 1)
            else:
                compare_set.append(new_sentence[1][i])
    # print(delete_list)
    delete_list.reverse()
    for position in delete_list:
        del new_sentence[1][position]
    return new_sentence


def open_txt(path):
    with open(path, encoding='utf-8') as file:
        matrix = file.read()
        matrix = matrix.rstrip()
    return matrix


def write_txt(state):
    if os.path.isfile('output.txt'):
        os.remove('output.txt')
    txt_name = 'output.txt'
    print_state = 'TRUE'

    if not state:
        print_state = 'FALSE'
    else:
        print_state = 'TRUE'
    with open(txt_name, 'a') as file:
        file.write(print_state)


def matrix_trans(matrix):
    rows = matrix.splitlines()
    temp_matrix = [row.split('\n') for row in rows if row.strip()]
    return np.array(temp_matrix)


def matrix_further_trans(matrix):
    rows = matrix
    temp_matrix = re.findall(r"\d+\.?\d*", rows)
    return np.ravel(temp_matrix)


def print_KB(tKB):
    for item in tKB:
        print(item)
    print('\n')
    return 0


def nagated_Query(sentence):
    for i in range(len(sentence[1])):
        item = sentence[1][i]
        if item == '|':
            sentence[1][i] = '&'
        elif item == '&':
            sentence[1][i] = '|'
        else:
            if '~' in item[0]:
                item[0] = item[0][1:]
            else:
                item[0] = '~' + item[0]
    return sentence


def fresh_KB(tKB):
    new_KB = []
    for sentence in tKB:
        if sentence[0] == 'CNF':
            sentence[0] = []
            new_KB.append(sentence)
    return new_KB


def change_KB_facts_p(tKB):
    new_KB = []
    for sentence in tKB:
        if len(sentence[1]) == 1:
            new_KB.insert(0, sentence)
        else:
            new_KB.append(sentence)
    return new_KB


def flatten(lst):
    flat_list = []
    for item in lst:
        if item != '|':
            if isinstance(item, list):
                flat_list.extend(flatten(item))
            else:
                flat_list.append(item)
    return flat_list


def check_if_in_KB(tKB, sentence):
    state = True
    for KB_sentence in tKB:
        # print(KB_sentence, sentence)
        if sorted(flatten(KB_sentence[1])) == sorted(flatten(sentence[1])):
            state = False

    return state


def add_same_pred_differp(tKB):
    new_KB = []
    return new_KB


def check_cannot_match2(sentence):
    new_sentence = copy.deepcopy(sentence)
    compare_list = []
    state = True
    name_set = set()
    # If Predicate and ~Predicate in same sentence, we cannot do that.
    for elements in new_sentence[1]:
        if elements != '|':
            if '~' in elements:
                if elements[0] not in name_set:
                    name_set.add(elements[0])
                else:
                    compare_list.append(elements[0])
            else:
                temp = '~' + elements[0]
                if temp not in name_set:
                    name_set.add(temp)
                else:
                    compare_list.append(temp)
    for name in name_set:
        compare_ele_list = []
        for elements in new_sentence[1]:
            if elements[0] in name:
                compare_ele_list.append(elements)

        for i in range(len(compare_ele_list)):
            # i start from the first element
            if '~' not in compare_ele_list[i][0]:
                for j in range(i+1, len(compare_ele_list)):
                    # we need to find ~Predicate
                    if '~' in compare_ele_list[j][0]:
                        if compare_ele_list[i][1:] == compare_ele_list[j][1:]:
                            state = False
            else:
                for j in range(i+1, len(compare_ele_list)):
                    # we need to find ~Predicate
                    if '~' not in compare_ele_list[j][0]:
                        if compare_ele_list[i][1:] == compare_ele_list[j][1:]:
                            state = False

    return state


def sort_KB(tKB):
    new_KB = []
    max_lens = 0
    for sentences in tKB:
        if max_lens <= len(sentences[1]):
            max_lens = len(sentences[1])
    # Get the maximum length
    for i in range(1, max_lens+1):
        for sentences in tKB:
            if len(sentences[1]) == i:
                new_KB.append(sentences)
    return new_KB


def simple_check(tKB, sentence):
    new_KB = copy.deepcopy(tKB)
    new_sentence = copy.deepcopy(sentence)
    simple_list = []
    for sentences in new_KB:
        # print(len(sentences[1]))
        if len(sentences[1]) == 1:
            simple_list.append(sentences)

    # We get all the facts
    # print(simple_list)
    temp_sentence = [[], []]
    for i in range(len(new_sentence[1])):
        if new_sentence[1][i] != '|':
            # print(new_sentence[1][i][1:])
            if '~' in new_sentence[1][i][0]:
                # we want to find the Predicate
                for s in range(len(simple_list)):
                    item = simple_list[s]
                    # print(item)
                    pred = item[1][0]
                    if '~' not in pred[0] and pred[0] in new_sentence[1][i][0] and pred[1:] == new_sentence[1][i][1:]:
                        break
                    if s == len(simple_list) - 1:
                            temp_sentence[1].append(new_sentence[1][i])
                            temp_sentence[1].append('|')
            else:
                # we want to find the ~Predicate
                compare = '~' + new_sentence[1][i][0]
                for s in range(len(simple_list)):
                    item = simple_list[s]
                    pred = item[1][0]
                    if '~' in pred[0] and pred[0] in compare and pred[1:] == new_sentence[1][i][1:]:
                        break
                    if s == len(simple_list) - 1:
                            temp_sentence[1].append(new_sentence[1][i])
                            temp_sentence[1].append('|')

    # print(f'This is the temp sentence', temp_sentence)
    if temp_sentence[1] != []:
        # print(f'This is the delete position', temp_sentence[1])
        del temp_sentence[1][-1]
    return temp_sentence


def multi_match_split(sentence):
    new_sentence = copy.deepcopy(sentence)
    split_list = []
    match_count = 0
    match_part = new_sentence[1]
    target_t = new_sentence[0]

    for elements in target_t[1]:
        if elements != '|':
            if elements[0] == match_part:
                match_count += 1

    if match_count == 1:
        split_list.append(new_sentence)
    else:
        for elements in target_t[1]:
            if elements != '|':
                if elements[0] == match_part:
                    temp_sentence = copy. deepcopy(target_t)
                    temp_sentence[1].insert(0, elements)
                    temp_sentence = delete_multi(temp_sentence)
                    split_list.append([temp_sentence, match_part])

    # print(split_list)

    return split_list


if __name__ == '__main__':
    '''t = ['CNF', [['~Order', 'x', 'y'], '|', ['Seated', 'x']]]
    t2 = [[[], [['~Seated', 'x'], '|', ['~Stocked', 'y'], '|', ['Order', 'x', 'y']]]]
    t3 = [[], [['~Stocked', 'y'], '|', ['~Seated', 'Bob'], '|', ['Order', 'x', 'y']]]
    print(check_if_in_KB(t2, t3))'''
    t = [[[], [['~MiniSudoku', 'Ac', 'B']]], [[], [['~MiniSudoku', 'Ac', 'A']]]]
    t2 = [[], [['MiniSudoku', 'Ac', 'B'], '|', ['MiniSudoku', 'Ac', 'A'], '|', ['MiniSudoku', 'Aa', 'B']]]
    t3 = [[[], [['MiniSudoku', 'Ac', 'B'], '|', ['MiniSudoku', 'Ac', 'A'], '|', ['MiniSudoku', 'Aa', 'B']]], 'MiniSudoku']
    t4 = [[[], [['MiniSudoku', 'Ac', 'B']]], 'MiniSudoku']
    # print(simple_check(t, t2))
    multi_match_split(t3)
    # t = nagated_Query(t)
    # print(t)
