import re
from utility import open_txt, matrix_trans


def no_infer(sentence):
    if re.findall(r'(.+)=>(.+)', sentence):
        return False
    else:
        return True


def re_triving_infer(sentence):
    lhs_re, rhs_re = [], []
    lhs_pred, lhs_var, rhs_pred, rhs_var = 0, 0, 0, 0

    # Format: A & B | C ... => D
    # Extract the left-hand and right-hand sides of the implication
    lhs, rhs = [side.strip() for side in re.findall(r'(.+)=>(.+)', sentence)[0]]
    # print(f'This is lhs and rhs', lhs, rhs)

    # Left
    # We need to deal with predicate1() & predicate2(), predicate1() | predicate2() two cases
    # we deal & case first

    # Get all operators [&, |]
    operators = re.findall(r'(&|\|)', lhs)
    # print(operators)

    lhs_list = [pred.strip() for pred in re.split('&|\|', lhs)]
    # print(lhs_list)
    for i in range(len(lhs_list)):
        lhs_pred = [re.findall(r'^(~?\w+)(?=\()', lhs_list[i])[0]]
        lhs_var = [s.strip() for s in re.findall(r'\w+\(([\w,\s]+)\)', lhs_list[i])[0].split(',')]
        lhs_re.append(lhs_pred + lhs_var)
        if i < len(lhs_list) - 1:
            lhs_re.append(operators[i])

    # Right Predicate(x,y)
    # Right side only contains one predicate, no need to extract here
    rhs_list = [pred.strip() for pred in rhs.split('&')]
    # print(rhs_list)
    for element in rhs_list:
        rhs_pred = [re.findall(r'^(~?\w+)(?=\()', element)[0]]  # will give the name of predicate, like Axe(x), give Axe
        rhs_var = [s.strip() for s in re.findall(r'\w+\(([\w,\s]+)\)', element)[0].split(',')]
        rhs_re.append(rhs_pred + rhs_var)

    # We will have the format: ['implies', [left predicates with its variable], [right predicates with its variable]]
    result = ['IMP', [], []]

    for item in lhs_re:
        result[1].append(item)

    for item in rhs_re:
        result[2].append(item)
    return result


def re_triving_noninfer(sentence):
    full_re = []

    operators = re.findall(r'(&|\|)', sentence)
    # print(operators)

    full_list = [pred.strip() for pred in re.split('&|\|', sentence)]
    # print(full_list)
    for i in range(len(full_list)):
        full_pred = [re.findall(r'^\s*(~)?\s*(\w+)\s*\(', full_list[i])[0]]
        if full_pred[0][0]:
            # Negated
            full_pred = ["~" + full_pred[0][1]]
        else:
            # Positive predicate name
            full_pred = [full_pred[0][1]]
        full_var = [s.strip() for s in re.findall(r'\w+\(([\w,\s]+)\)', full_list[i])[0].split(',')]
        full_re.append(full_pred + full_var)
        if i < len(full_list) - 1:
            full_re.append(operators[i])

    result = ['BCNF', []]

    for item in full_re:
        result[1].append(item)

    return result


if __name__ == '__main__':
    # t_matrix = open_txt('./Examples/input1.txt')
    t_matrix = open_txt('./Examples/special_case1.txt')
    t_matrix = matrix_trans(t_matrix)
    print(t_matrix[0][0])
    predict_sentence = t_matrix[0][0]
    print(f'No inference?', no_infer(predict_sentence))

    predict_sentence = re_triving_infer(predict_sentence)

    # print(isCNF(predict_sentence))
    # predict_sentence = re_triving_infer(predict_sentence)
    print(predict_sentence)