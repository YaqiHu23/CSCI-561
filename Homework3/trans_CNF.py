import copy
from deal_input import no_infer, re_triving_noninfer, re_triving_infer


def trans_IMP2BCNF(sentence):
    # Checked correct
    # sentence format: ['IMP', [left_items], [right_items]]
    re_sentence = copy.deepcopy(sentence)
    del re_sentence[2]
    re_sentence[0] = 'BCNF'
    # for items in re_sentence[1]:
    for count in range(len(re_sentence[1])):  # [[1], [2]]
        items = re_sentence[1][count]
        if items == '|':
            re_sentence[1][count] = '&'
        elif items == '&':
            re_sentence[1][count] = '|'
        elif items != '(' and items != ')':
            if count == len(re_sentence[1]) - 1:  # last element of left, change it operator to or
                if '~' in items[0]:
                    items[0] = items[0][1:]
                else:
                    items[0] = '~' + items[0]
                # re_sentence[1].append('|')
            else:
                # each item of left side of =>, need add a ~
                # We also need to deal with ~~
                if '~' in items[0]:
                    items[0] = items[0][1:]
                else:
                    items[0] = '~' + items[0]  # Predicate name to ~Predicate name
        # print(re_sentence[1][count])
    # print(f'This is the re_sentence IMP to BCNF', re_sentence)

    for items in sentence[2]:
        re_sentence[1].append('|')
        re_sentence[1].append(items)

    return re_sentence


def find_and_position(sentence):
    # Checked corrected
    re_sentence = copy.deepcopy(sentence)
    length = 0
    stack = []
    while length < len(re_sentence[1]):
        # print(length)
        if re_sentence[1][length] == '(':
            stack.append('(')
            pleft = length + 1
            while stack and pleft < len(re_sentence[1]):
                if re_sentence[1][pleft] == '(':
                    stack.append('(')
                elif re_sentence[1][pleft] == ')':
                    stack.pop()
                pleft += 1
            length = pleft
            continue
        elif re_sentence[1][length] == '&':
            return length
        length += 1
    return False


def add_parentheses(sentence):
    # Checked correct
    re_sentence = copy.deepcopy(sentence)

    position_and = []
    # re_sentence[1] is the [[predicate1, variables], [predicate2, variables], ......]
    # We find all the & position into a list
    position_and = find_and_position(re_sentence)
    # print(f'This is the and position', position_and)
    while position_and:
        # For each &, add ( to left , then add ) to right, until we reach an |
        # Dealing left
        left = position_and
        while left > -1:
            # print(left)
            if left == 0:
                re_sentence[1].insert(left, '(')
                break
            # if we meet a (), jump it
            elif re_sentence[1][left] == ')':
                lleft = left - 1
                while lleft > -1 and re_sentence[1][lleft] != '(':
                    lleft -= 1
                left = lleft
                continue
            elif re_sentence[1][left] == '|':
                re_sentence[1].insert(left + 1, '(')
                break
            left -= 1
        # print(re_sentence)
        # After add (, & position is position_and+1
        # Dealing right
        right = position_and + 1
        while right < len(re_sentence[1]):
            # print(f'This is the right', right)
            if right == len(re_sentence[1]) - 1:
                re_sentence[1].insert(right, ')')
                break

            # if we meet a (), jump it
            elif re_sentence[1][right] == '(':
                rright = right + 1
                while rright < len(sentence[1]) and re_sentence[1][rright] != ')':
                    rright += 1
                right = rright
                continue

            elif re_sentence[1][right] == '|':
                re_sentence[1].insert(right, ')')
                break
            right += 1
        position_and = find_and_position(re_sentence)
        # print(re_sentence)
        # print('hihi')
    return re_sentence


def collect_parentheses(sentence):
    # Checked corrected
    new_sentence = copy.deepcopy(sentence)
    del new_sentence[1][:]
    position_parentheses = []
    position_multi = []
    delete_position = set()

    left_parent_p = 0
    right_parent_p = 0

    for i in range(len(sentence[1])):

        if sentence[1][i] == '(':

            left_parent_p = i
            delete_position.add(i)
            j = i + 1
            while sentence[1][j] != ')':
                position_parentheses.append(sentence[1][j])
                delete_position.add(j)
                j += 1
            delete_position.add(j)
            right_parent_p = j
            break

    # In delete_position set, first element is (, last element is )
    # So we detect whether ( left has a element can multiple, or ) right has a element can multiple

    if left_parent_p > 1 and sentence[1][left_parent_p - 1] == '|':
        position_multi.append(sentence[1][left_parent_p - 2])
        delete_position.add(left_parent_p - 1)
        delete_position.add(left_parent_p - 2)
    elif right_parent_p < len(sentence[1]) - 2 and sentence[1][right_parent_p + 1] == '|':

        position_multi.append(sentence[1][right_parent_p + 2])
        delete_position.add(right_parent_p + 1)
        delete_position.add(right_parent_p + 2)

    # print(delete_position)
    for i in range(len(sentence[1])):
        if i not in delete_position:
            new_sentence[1].append(sentence[1][i])
    return new_sentence, position_parentheses, position_multi


def Isparet(sentence):
    for items in sentence[1]:
        if items == '(':
            return True
    return False


def detect_operator(sentence):
    state = False
    for item in sentence:
        if item == '&':
            state = True
    return state


def detect_only_and(sentence):
    state = True
    for item in sentence:
        if item == '|':
            state = False
    return state


def reduce_useless_parent(sentence):
    temp_sentence = copy.deepcopy(sentence)
    state = []
    # Find all () position
    positions = []
    stack = []
    all_state = []

    if not Isparet(sentence):
        return temp_sentence

    for i in range(len(temp_sentence[1])):
        if sentence[1][i] == "(":
            stack.append(i)
        elif sentence[1][i] == ")":
            positions.append([stack.pop(), i])
    for position in positions:
        all_state.append(detect_operator(temp_sentence[1][position[0]:position[1]]))
    if all(all_state):
        return temp_sentence

    state = all_state[0]
    # print(positions[0])
    if not state:
        del temp_sentence[1][positions[0][0]]
        # print(temp_sentence)
        del temp_sentence[1][positions[0][1] - 1]
    temp_sentence = reduce_useless_parent(temp_sentence)
    return temp_sentence


def cut_multiplier(sentence):
    new_sentence = []
    for item in sentence:
        new_sentence.append(item)

    temp_list = [[]]
    i = 0

    while new_sentence:
        item = new_sentence[0]
        # print(i, item)
        if item != '&':
            temp_list[i].append(item)
            new_sentence.remove(item)
        else:
            new_sentence.remove(item)
            i += 1
            temp_list.append([])
        # print(new_sentence, temp_list)
        # print('hihi\n')
    # we collect each clauses in multiplier A & B & C to A, B, C
    # print(temp_list)
    return temp_list


def distribution_law(sentence):
    re_sentence = []
    temp_sentence = copy.deepcopy(sentence)
    nest_type = False
    # After add parentheses, we apply distribution_law once
    # To apply law, we need to find one element before ( or after )
    # We use a new list to collect multiplier
    new_sentence, multiplier, multiplicand = collect_parentheses(temp_sentence)
    # print('This is multiplier before cut', multiplier)
    # We separate multiplier and multiplicand into two lists, then we divide them into two sentences
    # Multiplier size: At least 2
    multiplier = cut_multiplier(multiplier)
    # print('This is multiplier after cut', multiplier)
    # print('This is multiplicand', multiplicand)
    # print(f'This is size for multiplier', len(multiplier))
    for size in range(len(multiplier)):
        item = multiplier[size]
        # Format [ [Predicate1], [Predicate2], ... ]
        tar_sentence = ['CNF', []]
        for elements in item:
            tar_sentence[1].append(elements)
            tar_sentence[1].append('|')
        # Format ['CNF', [[Predicate1], '|', [Predicate2], ..., '|']]
        # print(tar_sentence)
        tar_sentence[1].append(multiplicand[0])
        re_sentence.append(tar_sentence)
    # print(f'This is the linked sentences', re_sentence)
    # print(f'This is the new sentence', new_sentence)
    # After divide, add least sentence[0][1] back to all new sentences,
    # If something is (......) |, then we add it ahead new sentence
    # If something is | (......), then we add it after new sentence
    add_position = 0
    if new_sentence[1]:
        for elements in new_sentence[1]:
            if elements != '|':
                if elements == '(':
                    for new_sens in re_sentence:
                        add_position = 1
                        new_sens[1].append('|')
                        new_sens[1].append(elements)
                elif elements == ')':
                    add_position = 0
                    for new_sens in re_sentence:
                        new_sens[1].append(elements)
                else:
                    if add_position == 0:
                        for new_sens in re_sentence:
                            new_sens[1].append('|')
                            new_sens[1].append(elements)
                    elif add_position == 1:
                        for new_sens in re_sentence:
                            new_sens[1].append(elements)

    # print(f'One distribution law appiled', re_sentence)

    # After that, we finish one time distribution law, we recurrsively apply it to all new sentences
    # call distribution_law()
    final_sentence = []

    for item in re_sentence:
        if Isparet(item):
            nest_type = True
            median_sentences = distribution_law(item)
            for each in median_sentences:
                final_sentence.append(each)
        else:
            final_sentence.append(item)
    # print(f'This is the final_sentence', final_sentence)
    if len(final_sentence) != 1:
        nest_type = True
    return final_sentence, nest_type


def trans_CNF(sentence):
    # We have two cases: BCNF need to transfer to CNF, IMP also need to transfer to CNF
    # Wanted sentence format: ['BCNF', [items]]
    median_sentence = []
    median_final_sentence = []
    nest_type = False
    re_sentence = []
    if sentence[0] == 'IMP':
        # We need to transfer IMP to BCNF first, and do BCNF
        median_sentence = trans_IMP2BCNF(sentence)
        # print(f'hihi', median_sentence)
    elif sentence[0] == 'BCNF':
        median_sentence = sentence
    # print(f'Before add () for BCNF', median_sentence)
    # Now the format together to ['BCNF', [items]]
    # Above checked corrected

    # Add parentheses to sentences to apply law
    # print(median_sentence)
    # If we have the sentence only have & like A & B, we just split it:
    if detect_only_and(median_sentence[1]):
        for item in median_sentence[1]:
            if item != '&' and item != '(' and item != ')':
                temp = ['CNF', [item]]
                re_sentence.append(temp)
                nest_type = 3
                # print(re_sentence)
    else:
        median_sentence = add_parentheses(median_sentence)
        # print(f'After add () for BCNF', median_sentence)
        # We need to apply distribution law
        # From A or (B and C) to (A or B) and (A or C)

        median_sentence = reduce_useless_parent(median_sentence)
        # print(f'After delete ()', median_sentence)

        if Isparet(median_sentence):
            re_sentence, nest_type = distribution_law(median_sentence)
        else:
            median_sentence[0] = 'CNF'
            re_sentence = median_sentence
        # After apply distribution law, we have the format ['CNF', [items]]
        # re_sentence maybe a nested function, [['CNF', [items]], ['CNF', [items]]]
    return re_sentence, nest_type


def cluster_CNF(sentence):
    # Divided one CNF sentence into several CNF sentences
    # (A or B) and (A or C) to   A or B    A or C
    re_sentence = sentence
    # Add sentences into KB
    return re_sentence


def extract_sentences(tKB):
    target_KB = []
    nest_type = False

    for item in tKB:
        final_sentences = []
        if no_infer(item):
            t_sentence = re_triving_noninfer(item)
            t_sentence = add_parentheses(t_sentence)
            # print(f'This is first add parentheses', t_sentence)
            t_sentence, nest_type = trans_CNF(t_sentence)
            # Notice, one sentence may divide into several sentences
            final_sentences.append(cluster_CNF(t_sentence))
            # print(final_sentences)
            # Add sentences to new target_KB
            # print(f'One Final Sentence', len(final_sentences))
            # print(f'This is the final sentence', final_sentences)
            # print(nest_type)
            if not nest_type:
                target_KB.append(final_sentences[0])
            elif nest_type == 3:
                for items in final_sentences[0]:
                    target_KB.append(items)
            else:
                for items in final_sentences:
                    # print(items)
                    target_KB.append(items)
        else:
            t_sentence = re_triving_infer(item)
            t_sentence = add_parentheses(t_sentence)
            # print(f'This is first add parentheses', t_sentence)
            # print(f'After first add parentheses', t_sentence)
            t_sentence, nest_type = trans_CNF(t_sentence)
            # Notice, one sentence may divide into several sentences
            final_sentences.append(cluster_CNF(t_sentence))
            # print(final_sentences)
            # Add sentences to new target_KB
            # print(f'This is final_sentence[0]', final_sentences[0])

            if not nest_type:
                target_KB.append(final_sentences[0])
            else:
                for items in final_sentences[0]:
                    target_KB.append(items)

    return target_KB


if __name__ == '__main__':
    '''
    KB_sentence = []
    t_matrix = open_txt('./Examples/input1.txt')
    t_matrix = matrix_trans(t_matrix)
    KB = []
    Query = re_triving_noninfer(t_matrix[0][0])

    print(f'This is the Query\n', Query)
    KB_size = int(t_matrix[1])
    for i in range(2, KB_size + 2):
        KB.append(t_matrix[i][0])
    print(f'This is the KB\n', KB)

    KB = extract_sentences(KB)
    print(f'This is transferred BCNF KB\n', KB)
    '''
    t = [['BCNF', [['~Order', 'x', 'y'], '|', ['Seated', 'x']]]]
    t2 = [['BCNF', ['(', ['~GetCheck', 'x'], '&', ['~Paid', 'x'], ')', '|', ['Leave', 'x']]]]
    t3 = [['BCNF', [['Leave', 'x'], '|', '(', ['~GetCheck', 'x'], '&', ['~Paid', 'x'], ')']]]
    t4 = [['BCNF', [['D'], '|', ['A'], '|', '(', ['B'], '&', ['C'], ')', '|', '(', ['E'], '&', ['D'], ')']]]
    t5 = [['BCNF', [['D'], '|', ['A'], '|', '(', ['B'], '&', ['C'], ')', '|', '(', ['E'], '&', ['D'], ')']]]
    t6 = ['BCNF', [['~Likes', 'x', 'y'], '|', ['~Likes', 'y', 'x'], '&', ['~Meet', 'x', 'y', 'z']]]
    print(t6)
    # t6 = cut_multiplier(t6)
    t6 = distribution_law(t6)
    # print(t3)
    # t = add_parentheses(t)
    # t2, mull, mulr = collect_parentheses(t2)
    # t3 = distribution_law(t3)
    # print(t)
    # print(t3)
    # print(mull)
    # print(mulr)
