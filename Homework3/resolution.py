import copy
import time
from utility import print_KB, check_if_in_KB, change_KB_facts_p, check_cannot_match2, sort_KB, simple_check, delete_multi, multi_match_split


def substitution_sentence(sentence):
    new_sentence = copy.deepcopy(sentence)
    # Format [[[x], [y], ...], [[predicate1], [predicate2], ...]]
    # print('This is the new_sentence[0]', new_sentence[0])
    for var in new_sentence[0]:
        # print(f'This is the var', var)
        # Format [x, 'Name']
        for element in new_sentence[1]:
            # Format [Predicatename, x, y]
            for i in range(len(element[1:])):
                if element[i + 1][0].islower():
                    if var[0] == element[i + 1]:
                        # Match variable x == x
                        element[i + 1] = var[1]

    return new_sentence


def match_variables(original, target):
    match_list = []
    left_sentence_var = []
    same_list = []
    match_state = True
    # Format: finder_sentence, [each_match, same part]
    same_part = target[1]
    target_sentence = target[0]
    # if same_part has a ~, which is ~Predicate, it means we want to find Predicate in original, ~Predicate in target
    # if not has a ~, which is Predicate name, then we want to find ~Predicate in original, Predicate in target
    if '~' in same_part:
        for item in original[1]:
            if item[0] in same_part:
                # predicate name is match
                left_sentence_var = item[1:]
    else:
        compare = '~' + same_part
        for item in original[1]:
            if item[0] == compare:
                left_sentence_var = item[1:]
    # print(left_sentence_var)

    # print(f'This is the left_sentence_var', left_sentence_var)
    # print(f'This is the target sentence', target_sentence)
    # print(f'This is the same part', same_part)
    for item in target_sentence[1]:
        # Format: [ [Predicate1], [Predicate2], ... ]
        # print(f'Each item in target_sentence[1]', item)
        if item[0] == same_part and item != '|':
            same_list.append(item)
    for item in same_list:
        # print(f'This is the item[0]', item)
        match_state = True
        for i in range(len(left_sentence_var)):
            # print(lvar, var)
            lvar = left_sentence_var[i]
            var = item[i + 1]
            link_var = []
            # Deal with left constant, right constant
            if lvar[0].isupper() and var[0].isupper() and var == lvar:
                link_var = [lvar, var]
            # Deal with left constant, right var
            elif lvar[0].isupper() and var[0].islower():
                link_var = [var, lvar]
            # Deal with left var, right constant
            elif lvar[0].islower() and var[0].isupper():
                link_var = [lvar, var]
            # Deal with left var, right var
            elif lvar[0].islower() and var[0].islower():
                # print('1')
                link_var = [lvar, var]
            # print(link_var)
            if link_var == []:
                match_state = False
                break
            else:
                match_list.append(link_var)

        if match_state == True:
            return match_list, match_state

    return match_list, match_state


def link_sentences(variables, original, target):
    # Checked Correnct
    new_sentence = [[], []]
    # The original sentence and target sentence may their variable part, with the new variables part
    # variables, finder_sentence, each_match
    same_part = target[1]
    target_sentence = target[0]

    for item in variables:
        original[0].append(item)
        target_sentence[0].append(item)

    original = substitution_sentence(original)
    target_sentence = substitution_sentence(target_sentence)

    # print(f'This is the original sentence', original)
    # print(f'This is the target sentence', target_sentence)
    # We copy all the variables to the new sentence
    # Next we link old sentence with target sentence
    # if same_part has a ~, which is ~Predicate, it means we want to find Predicate in original, ~Predicate in target
    # if not has a ~, which is Predicate name, then we want to find ~Predicate in original, Predicate in target
    for element in original[1]:
        count = 0
        # print(element)
        if element != '|':
            if '~' in element[0]:
                compare = element[0][1:]
            else:
                compare = element[0]

            if '~' in same_part:
                # It means we will cancel Predicate in finder sentence
                if '~' not in element[0] and element[0] in same_part:
                    r_vars = element[1:]
                    # print(r_vars)
                    for item in r_vars:
                        # Format x or y or z, ...
                        if variables[count][0][0].isupper() and item != variables[count][0]:
                            new_sentence[1].append(element)
                            new_sentence[1].append('|')
                            break
                        elif variables[count][0][0].islower() and item != variables[count][1]:
                            new_sentence[1].append(element)
                            new_sentence[1].append('|')
                            break
                        count += 1
                else:
                    new_sentence[1].append(element)
                    new_sentence[1].append('|')
            else:
                if '~' in element[0] and element[0][1:] in same_part:
                    r_vars = element[1:]
                    # print(r_vars)
                    for item in r_vars:
                        # Format x or y or z, ...
                        # print()
                        if variables[count][0][0].isupper() and item != variables[count][0]:
                            new_sentence[1].append(element)
                            new_sentence[1].append('|')
                            break
                        elif variables[count][0][0].islower() and item != variables[count][1]:
                            new_sentence[1].append(element)
                            new_sentence[1].append('|')
                            break
                        count += 1
                else:
                    new_sentence[1].append(element)
                    new_sentence[1].append('|')

            # if not, just append
            if compare not in same_part:
                new_sentence[1].append(element)
                new_sentence[1].append('|')

    for element in target_sentence[1]:
        count = 0
        if element != '|':
            if '~' in element[0]:
                compare = element[0][1:]
            else:
                compare = element[0]

            if '~' in same_part:
                # It means we will cancel ~Predicate in target
                if '~' in element[0] and element[0] == same_part:
                    # if the predicate name is same as the match, we need to check the vars are same
                    # For all vars in next, if it is not equals to all vars match, we need also link them
                    r_vars = element[1:]
                    # print(r_vars)
                    for item in r_vars:
                        # print(f'hihi', variables[count][0][0].isupper())
                        # Format x or y or z, ...
                        if variables[count][0][0].isupper() and item != variables[count][0]:
                            # print(f'something')
                            new_sentence[1].append(element)
                            new_sentence[1].append('|')
                            break
                        elif variables[count][0][0].islower() and item != variables[count][1]:
                            new_sentence[1].append(element)
                            new_sentence[1].append('|')
                            break
                        count += 1
                else:
                    new_sentence[1].append(element)
                    new_sentence[1].append('|')
            else:
                # It means we will cancel ~Predicate in target
                if '~' not in element[0] and element[0] in same_part:
                    # if the predicate name is same as the match, we need to check the vars are same

                    # For all vars in next, if it is not equals to all vars match, we need also link them
                    r_vars = element[1:]
                    # print(r_vars)
                    for item in r_vars:
                        # Format x or y or z, ...
                        if variables[count][0][0].isupper() and item != variables[count][0]:
                            new_sentence[1].append(element)
                            new_sentence[1].append('|')
                            break
                        elif variables[count][0][0].islower() and item != variables[count][1]:
                            new_sentence[1].append(element)
                            new_sentence[1].append('|')
                            break
                        count += 1
                else:
                    new_sentence[1].append(element)
                    new_sentence[1].append('|')

            # if not, just append
            if compare not in same_part:
                new_sentence[1].append(element)
                new_sentence[1].append('|')
    # We always add one more '|'
    if new_sentence[1]:
        del new_sentence[1][-1]
    return new_sentence


def fresh_variables(sentence):
    new_sentence = copy.deepcopy(sentence)
    new_sentence[0] = []
    return new_sentence


def same_var_same_check(variables):
    new_variables = copy.deepcopy(variables)
    state = True
    variable_set = set(sublist[0] for sublist in new_variables)
    if len(variable_set) != len(new_variables):
        state = False
        return state

    return state


def change_vars_intarget(finder_sentence, sentence):
    new_sentence = copy.deepcopy(sentence)
    finder_vars = []
    for item in finder_sentence[1]:
        if item != '|':
            # Format: [[P1, vars], [P2, vars], ...]
            for svars in item[1:]:
                if svars.islower():
                    finder_vars.append(svars)
    # print(finder_vars)
    for item in new_sentence[1]:
        # print(item)
        if item != '|':
            # Format: [[P1, vars], [P2, vars], ...]
            for i in range(len(item[1:])):
                svars = item[i+1]
                # print(svars)
                if svars in finder_vars:
                    # print(1)
                    item[i+1] = svars + svars
    return new_sentence


def change_vars_back(sentence):
    new_sentence = copy.deepcopy(sentence)
    for i in range(len(new_sentence[1])):
        item = new_sentence[1][i]
        # print(item)
        if item != '|':
            for pvars in range(len(item[1:])):
                # print(item[pvars+1])
                # print(item[pvars+1].islower())
                if item[pvars+1].islower() and len(item[pvars+1]) != 1:
                    new_sentence[1][i][pvars+1] = new_sentence[1][i][pvars+1][0]
    return new_sentence


def unification(tKB, finder_sentence):
    state = False
    change_state = False
    match_list = []
    match_state = True
    new_KB = copy.deepcopy(tKB)
    # for each element in finder_sentence[1], we want to unify it
    # print(f'This is the finder sentence', finder_sentence)
    # print(f'This is the KB', new_KB)
    # print_KB(new_KB)

    match_list = []
    i = 0
    for element in finder_sentence[1]:
        match_list.append([])
        if element != '|':
            # format [predicate_name, variables]
            if '~' in element[0]:
                # For a ~Predicate, we want to find Predicate
                temp_name = element[0][1:]
                # Predicate
                for sentence in new_KB:
                    # format [[], [[1], [2],...]]
                    for item in sentence[1]:
                        if item != '|':
                            # format [predicate_name, variables]
                            if temp_name == item[0]:
                                match_list[i].append([sentence, element[0][1:]])

            else:
                temp_name = '~' + element[0]
                # For each Predicate, we want to find ~Predicate
                for sentence in new_KB:
                    # print(f'The sentence from KB', sentence)
                    # format [[], [[1], [2],...]]
                    for item in sentence[1]:
                        if item != '|':
                            # format [predicate_name, variables]
                            if temp_name == item[0]:
                                match_list[i].append([sentence, temp_name])

    # print(f'This is the match list', match_list)

    # Correct above
    # We find all the match variable to see whether it is worth matching
    # container = []
    if match_list:
        # for each_match in match_list:
        for j in range(len(match_list)):
            for i in range(len(match_list[j])):
                median_sentence = []
                each_matches = match_list[j][i]
                multi_list = multi_match_split(each_matches)
                for each_match in multi_list:
                    # print(f'This is the match sentence', each_match)
                    # We need to change vars different from match_list
                    each_match[0] = change_vars_intarget(finder_sentence, each_match[0])
                    variables, match_state = match_variables(finder_sentence, each_match)
                    # print(f'This is the variables', variables)
                    # format of variables [ [x, namex], [y, namey], ... ]
                    # print(f'This is the each match', each_match[0])
                    # print(f'This is the match state', match_state)
                    var_state = same_var_same_check(variables)
                    if match_state and var_state:
                        # If we can unify their variables, then we can unify them, otherwise, fail
                        # If we can unify, delete old sentence
                        # new_KB.remove(change_vars_back(each_match[0]))
                        median_sentence = link_sentences(variables, finder_sentence, each_match)
                        conter_state = check_cannot_match2(median_sentence)
                        if conter_state == False:
                            continue
                        # print(f'This is the linked sentence before delete multi', median_sentence)
                        median_sentence = delete_multi(median_sentence)
                        # If we find one empty, then we get the answer, we finish and break
                        # print(f'This is the linked sentence', median_sentence)
                        if not median_sentence[1]:
                            state = True
                            return new_KB, state, change_state
                        # We get the median sentence, next we need to substitution it to all variables
                        # median_sentence = substitution_sentence(median_sentence)
                        median_sentence = fresh_variables(median_sentence)
                        median_sentence = change_vars_back(median_sentence)
                        # print(f'This is the final sentence', median_sentence)
                        # After substitution, one resolution is finished, next we do it on the new KB
                        median_sentence = simple_check(new_KB, median_sentence)
                        # print(f'This is the final sentence', median_sentence)
                        if median_sentence[1] == []:
                            state = True
                            return new_KB, state, change_state

                        in_state = check_if_in_KB(new_KB, median_sentence)

                        # container.append(in_state)
                        # print(container)
                        # in_state is True if we can insert to new_KB
                        # print(f'jump state', i == len(match_list) - 1 and all(container) == False)
                        if in_state == True:
                            change_state = True
                            new_KB.append(median_sentence)
                            # print(f'This is the KB after one resolution')
                            # print_KB(new_KB)

    # print(f'This is the KB after one resolution')
    # print_KB(new_KB)
    # print(f'hi', change_state)
    return new_KB, state, change_state


def resolution_function(tKB, run_time):
    resolution_state = False
    change_state = True
    temp_KB = copy.deepcopy(tKB)
    i = 0
    # For each sentence in tKB, we need to find which sentences in tKB can unify with it
    # We do resolution until find one empty, that is resolution_state is true
    # Or if we reach the end of the temp_KB, which means no sentence can unify with another one, we fail

    while 1:
        end_time = time.time()
        if end_time - run_time > 900:
            print('Time out, False')
            return False
        if len(temp_KB) >= 1000:
            print('Too many sentences')
            return False

        if i < len(temp_KB) and change_state:
            temp_KB, resolution_state, change_state = unification(temp_KB, temp_KB[i])
            if change_state:
                temp_KB = change_KB_facts_p(temp_KB)
                temp_KB = sort_KB(temp_KB)
                i = 0
            if resolution_state:
                return resolution_state
        elif i == len(temp_KB):
            break
        else:
            # print(f'No change i', i)
            i += 1
            change_state = True
    return resolution_state


if __name__ == '__main__':
    t1 = [[], [['~Open', 'Kitchen']]]
    t2 = [[], [['~Seated', 'x'], '|', ['Open', 'Restaurant']]]
    fKB = []
    fKB.append(t1)
    fKB.append(t2)
    # t3 = [[['x', 'Kitchen']], [['~Open', 'Kitchen']]]
    t5 = [[], [['~Open', 'Kitchen']]]
    t4 = [[[], [['~Seated', 'x'], '|', ['Open', 'y']]], '~Open']
    t6 = [[['y', 'Kitchen']], [['~Seated', 'x'], '|', ['Open', 'y']]]
    t7 = [[['y', 'Kitchen']], [['~Seated', 'x'], '|', ['~Seated', 'x'], '|', ['Open', 'y'], '|', ['Open', 'y']]]
    t8 = [['~Open', 'Restaurant'], '|', ['~Open', 'Kitchen'], '|', ['Seated', 'x']]
    t9 = [[], [['~Stocked', 'Pasta'], '|', ['Stocked', 'Italian']]]
    t10 = [[[], [['~Stocked', 'Flour'], '|', ['~Stocked', 'Cheese'], '|', ['Stocked', 'Pasta']]], 'Stocked']
    t11 = [[], [['~Seated', 'x'], '|', ['~Stocked', 'y'], '|', ['Order', 'x', 'y']]]
    t12 = [[[], [['~Order', 'x', 'y'], '|', ['Ate', 'x']]], '~Order']
    t13 = [[], [['~Leave', 'Helena']]]
    t14 = [[[], [['~Ate', 'x'], '|', ['~HaveMoney', 'x'], '|', ['Leave', 'x']]], 'Leave']
    t15 = [[], [['~MiniSudoku', 'Ac', 'D']]]
    t16 = [[[], [['MiniSudoku', 'Aa', 'x'], '|', ['MiniSudoku', 'Ab', 'x'], '|', ['MiniSudoku', 'Ac', 'x'], '|',
                 ['MiniSudoku', 'Ad', 'x']]], 'MiniSudoku']
    t17 = [[], [['~Seated', 'x'], '|', ['~Stocked', 'y'], '|', ['Order', 'x', 'y']]]
    t18 = [[[], [['~Order', 'x', 'y'], '|', ['Ate', 'x']]], '~Order']
    t19 = [[], [['~Ate', 'x'], '|', ['GetCheck', 'x']]]
    t20 = [[[], [['~Ate', 'x'], '|', ['GetCheck', 'x']]], [[], [['~GetCheck', 'x'], '|', ['~HaveMoney', 'x'], '|', ['Paid', 'x']]], [[], [['~Order', 'x', 'y'], '|', ['Ate', 'x']]]]
    # temp = link_sentences([], t3, t4)
    # temp = match_variables(t5, t4)
    # temp2 = link_sentences(temp, t5, t4)
    # temp2 = fresh_variables(temp2)
    # print(t7)
    # temp3 = delete_multi(t8)
    # print(t20)
    # print(t19)
    temp4 = unification(t20, t19)
    print(temp4)
    # temp3 = substitution_sentence(t6)
    # print(temp)
    # print(temp2)
    # print(temp3)
