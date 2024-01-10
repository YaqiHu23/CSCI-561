import os
import numpy as np
from queue import Queue
import re

def open_txt(path):
    with open('./hw1/input40.txt', encoding='utf-8') as file:
        matrix = file.read()
        matrix = matrix.rstrip()
    return matrix


def write_txt(path, path_number, count):
    new_path = []
    output = 0
    i = len(path)

    if path_number > 1:
        if count == 0:
            if os.path.isfile('output.txt'):
                os.remove('output.txt')

        if path == 'FAIL':
            with open('output.txt', 'a') as file:
                file.write('FAIL')
                file.write('\n')
        else:
            while i > 0:
                new_path.append(path[i - 1])
                i = i - 1
            # print(new_path)

            with open('output.txt', 'a') as file:
                for i in range(len(new_path)):
                    output = ','.join(str(i) for i in new_path[i])
                    # print(output)
                    file.write(output + ' ')
                file.write('\n')
        count = count + 1
        return count
    else:
        if os.path.isfile('output.txt'):
            os.remove('output.txt')
        txt_name = 'output.txt'

        if path == 'FAIL':
            with open(txt_name, 'a') as file:
                file.write('FAIL')
        else:
            while i > 0:
                new_path.append(path[i - 1])
                i = i - 1
            # print(new_path)

            with open(txt_name, 'a') as file:
                for i in range(len(new_path)):
                    output = ','.join(str(i) for i in new_path[i])
                    # print(output)
                    file.write(output + ' ')


def matrix_trans(matrix):
    rows = matrix.splitlines()
    temp_matrix = [row.split('\n') for row in rows if row.strip()]
    return np.array(temp_matrix)


def matrix_further_trans(matrix):
    rows = matrix
    temp_matrix = re.findall(r"\d+\.?\d*", rows)
    return np.ravel(temp_matrix)


def bfs_algorithm(matrix, target_l, target_r, uer_stamina, W, H, start_l, start_r):
    current_value = matrix[start_r][start_l]
    # Now find road to next
    path = []
    current_l = start_l
    current_r = start_r
    position = 0

    path_map = np.zeros([H, W], int)

    start = [current_l, current_r]
    queue = Queue()
    appear = []

    adj_arr = []

    queue.put(start)
    appear.append(start)

    new_list = [[start_l, start_r,current_value, []]]

    while (current_l != target_l or current_r != target_r) and not queue.empty():
        current = queue.get()
        current_value = matrix[current_r][current_l]
        # print(current)
        current_l = current[0]
        current_r = current[1]
        # print(f'This is the current position', current_l, current_r)
        # print(f'This is the current value', current_value)
        if W > current_l >= 0 and H > current_r >= 0:
            # we are in the map now
            # test 8-directions
            if W > current_l - 1 >= 0 and H > current_r - 1 >= 0:
                # left up point
                if current_value > 0 and matrix[current_r - 1][current_l - 1] > 0 and current_value - \
                        matrix[current_r - 1][current_l - 1] >= 0:
                    left_up_value = abs(current_value - matrix[current_r - 1][current_l - 1])
                    adj_arr.append([current_l - 1, current_r - 1, left_up_value, []])
                elif matrix[current_r - 1][current_l - 1] < 0 and abs(current_value) >= abs(
                        matrix[current_r - 1][current_l - 1]):
                    left_up_value = abs(current_value - matrix[current_r - 1][current_l - 1])
                    adj_arr.append([current_l - 1, current_r - 1, left_up_value, []])
                elif abs(current_value - matrix[current_r - 1][current_l - 1]) <= uer_stamina:
                    left_up_value = abs(current_value - matrix[current_r - 1][current_l - 1])
                    adj_arr.append([current_l - 1, current_r - 1, left_up_value, []])

            if 0 <= current_r - 1 < H:
                # up point
                if current_value > 0 and matrix[current_r - 1][current_l] > 0 and current_value - matrix[current_r - 1][
                    current_l] >= 0:
                    up_value = abs(current_value - matrix[current_r - 1][current_l])
                    adj_arr.append([current_l, current_r - 1, up_value, []])
                elif matrix[current_r - 1][current_l] < 0 and abs(current_value) >= abs(
                        matrix[current_r - 1][current_l]):
                    up_value = abs(current_value - matrix[current_r - 1][current_l])
                    adj_arr.append([current_l, current_r - 1, up_value, []])
                elif abs(current_value - matrix[current_r - 1][current_l]) <= uer_stamina:
                    up_value = abs(current_value - matrix[current_r - 1][current_l])
                    adj_arr.append([current_l, current_r - 1, up_value, []])

            if H > current_r - 1 >= 0 and 0 <= current_l + 1 < W:
                # right up point
                if current_value > 0 and matrix[current_r - 1][current_l + 1] > 0 and current_value - \
                        matrix[current_r - 1][current_l + 1] >= 0:
                    right_up_value = abs(current_value - matrix[current_r - 1][current_l + 1])
                    adj_arr.append([current_l + 1, current_r - 1, right_up_value, []])
                elif matrix[current_r - 1][current_l + 1] < 0 and abs(current_value) >= abs(
                        matrix[current_r - 1][current_l + 1]):
                    right_up_value = abs(current_value - matrix[current_r - 1][current_l + 1])
                    adj_arr.append([current_l + 1, current_r - 1, right_up_value, []])
                elif abs(current_value - matrix[current_r - 1][current_l + 1]) <= uer_stamina:
                    right_up_value = abs(current_value - matrix[current_r - 1][current_l + 1])
                    adj_arr.append([current_l + 1, current_r - 1, right_up_value, []])

            if 0 <= current_l + 1 < W:
                # right point
                if current_value > 0 and matrix[current_r][current_l + 1] > 0 and current_value - matrix[current_r][
                    current_l + 1] >= 0:
                    right_value = abs(current_value - matrix[current_r][current_l + 1])
                    adj_arr.append([current_l + 1, current_r, right_value, []])
                elif matrix[current_r][current_l + 1] < 0 and abs(current_value) >= abs(
                        matrix[current_r][current_l + 1]):
                    right_value = abs(current_value - matrix[current_r][current_l + 1])
                    adj_arr.append([current_l + 1, current_r, right_value, []])
                elif abs(current_value - matrix[current_r][current_l + 1]) <= uer_stamina:
                    right_value = abs(current_value - matrix[current_r][current_l + 1])
                    adj_arr.append([current_l + 1, current_r, right_value, []])

            if 0 <= current_l + 1 < W and 0 <= current_r + 1 < H:
                # right low point
                if current_value > 0 and matrix[current_r + 1][current_l + 1] > 0 and current_value - \
                        matrix[current_r + 1][current_l + 1] >= 0:
                    right_up_value = abs(current_value - matrix[current_r + 1][current_l + 1])
                    adj_arr.append([current_l + 1, current_r + 1, right_up_value, []])
                elif matrix[current_r + 1][current_l + 1] < 0 and abs(current_value) >= abs(
                        matrix[current_r + 1][current_l + 1]):
                    right_up_value = abs(current_value - matrix[current_r + 1][current_l + 1])
                    adj_arr.append([current_l + 1, current_r + 1, right_up_value, []])
                elif abs(current_value - matrix[current_r + 1][current_l + 1]) <= uer_stamina:
                    right_up_value = abs(current_value - matrix[current_r + 1][current_l + 1])
                    adj_arr.append([current_l + 1, current_r + 1, right_up_value, []])

            if 0 <= current_l - 1 < W and H > current_r + 1 >= 0:
                # left low point
                if current_value > 0 and matrix[current_r + 1][current_l - 1] > 0 and current_value - \
                        matrix[current_r + 1][current_l - 1] >= 0:
                    left_low_value = abs(current_value - matrix[current_r + 1][current_l - 1])
                    adj_arr.append([current_l - 1, current_r + 1, left_low_value, []])
                elif matrix[current_r + 1][current_l - 1] < 0 and abs(current_value) >= abs(
                        matrix[current_r + 1][current_l - 1]):
                    left_low_value = abs(current_value - matrix[current_r + 1][current_l - 1])
                    adj_arr.append([current_l - 1, current_r + 1, left_low_value, []])
                elif abs(current_value - matrix[current_r + 1][current_l - 1]) <= uer_stamina:
                    left_low_value = abs(current_value - matrix[current_r + 1][current_l - 1])
                    adj_arr.append([current_l - 1, current_r + 1, left_low_value, []])

            if 0 <= current_r + 1 < H and W > current_l >= 0:
                # low point
                if current_value > 0 and matrix[current_r + 1][current_l] > 0 and current_value - matrix[current_r + 1][
                    current_l] >= 0:
                    low_value = abs(current_value - matrix[current_r + 1][current_l])
                    adj_arr.append([current_l, current_r + 1, low_value, []])
                elif matrix[current_r + 1][current_l] < 0 and abs(current_value) >= abs(
                        matrix[current_r + 1][current_l]):
                    low_value = abs(current_value - matrix[current_r + 1][current_l])
                    adj_arr.append([current_l, current_r + 1, low_value, []])
                elif abs(current_value - matrix[current_r + 1][current_l]) <= uer_stamina:
                    low_value = abs(current_value - matrix[current_r + 1][current_l])
                    adj_arr.append([current_l, current_r + 1, low_value, []])

            if W > current_l - 1 >= 0 and H > current_r >= 0:
                # left point
                if current_value > 0 and matrix[current_r][current_l - 1] > 0 and current_value - matrix[current_r][
                    current_l - 1] >= 0:
                    left_value = abs(current_value - matrix[current_r][current_l - 1])
                    adj_arr.append([current_l - 1, current_r, left_value, []])
                elif matrix[current_r][current_l - 1] < 0 and abs(current_value) >= abs(
                        matrix[current_r][current_l - 1]):
                    left_value = abs(current_value - matrix[current_r][current_l - 1])
                    adj_arr.append([current_l - 1, current_r, left_value, []])
                elif abs(current_value - matrix[current_r][current_l - 1]) <= uer_stamina:
                    left_value = abs(current_value - matrix[current_r][current_l - 1])
                    adj_arr.append([current_l - 1, current_r, left_value, []])
        else:
            # print('FAIL')
            return 'FAIL'

        # print(f'This is adj_arr', adj_arr)

        new_adj_list = []
        # Delete the position used
        for i in range(len(adj_arr)):
            point = [adj_arr[i][0], adj_arr[i][1]]
            if point not in appear:
                new_adj_list.append(adj_arr[i])
        # print(f'This is the new_adj', new_adj_list)

        adj_arr = new_adj_list

        # Add the non-used points to queue
        for i in range(len(adj_arr)):
            point = [adj_arr[i][0], adj_arr[i][1]]
            if path_map[current_r, current_l] + 1 > path_map[adj_arr[i][1], adj_arr[i][0]]:
                # print(f'the current', current)
                adj_arr[i][3] = current
                new_list.append(adj_arr[i])
                path_map[adj_arr[i][1], adj_arr[i][0]] = path_map[current_r, current_l] + 1
            queue.put(point)
            appear.append(point)
        # print(f'This is the queue', queue.qsize())
        # print(f'This is path map', path_map)
        # print(f'This is new list', new_list)

        if current_l != target_l and current_r != target_l and queue.empty():
            return 'FAIL'
    # Search work finished, then we start from tail to head

    for i in range(len(new_list)):
        if target_l == new_list[i][0] and target_r == new_list[i][1]:
            position = i

    back_parent = new_list[position]
    while back_parent[0] != start_l or back_parent[1] != start_r:
        # print(f'This is the back', back_parent)
        parent = back_parent[3]
        # print(f'this is the small parent', parent)
        path.append([back_parent[0], back_parent[1]])
        # we find the parent
        for i in range(len(new_list)):
            if parent[0] == new_list[i][0] and parent[1] == new_list[i][1]:
                position = i

        # print(f'This is the parent', new_list[position])
        back_parent = new_list[position]
        # print(f'This is the back_parent', back_parent)
    path.append([start_l, start_r])
    # print(f'This is the path', path)
    return path


def bfs_method(matrix, target_point_list, target_point_num, uer_stamina, W, H, start_l, start_r):
    # find all the path from start_point_list
    count_p = 0
    if target_point_num == 1:
        target_l = target_point_list[0]
        target_r = target_point_list[1]
        path = bfs_algorithm(matrix, target_l, target_r, uer_stamina, W, H, start_l, start_r)
        count_p = write_txt(path, target_point_num, count_p)
    else:
        for k in range(target_point_num):
            target_current = target_point_list[k]
            target_l = target_current[0]
            target_r = target_current[1]
            path = bfs_algorithm(matrix, target_l, target_r, uer_stamina, W, H, start_l, start_r)
            count_p = write_txt(path, target_point_num, count_p)


def find_position_in_queue(queue, element):
    new_queue = Queue()
    position = []
    while not queue.empty():
        c_value = queue.get()
        new_queue.put(c_value)
        if element[0] == c_value[0] and element[1] == c_value[1]:
            position = c_value
    if not position:
        return [new_queue, 0]
    else:
        return [new_queue, position]


def Delete_position_in_queue(queue, element):
    new_queue = Queue()
    while not queue.empty():
        c_value = queue.get()
        if element[0] == c_value[0] and element[1] == c_value[1]:
            continue
        else:
            new_queue.put(c_value)
    queue = new_queue
    return queue


def find_position_in_list(f_list, element):
    for i in range(len(f_list)):
        if element[0] == f_list[i][0] and element[1] == f_list[i][1]:
            return f_list[i]


def Delete_position_in_list(f_list, element):
    for i in range(len(f_list)):
        if element[0] == f_list[i][0] and element[1] == f_list[i][1]:
            f_list.pop(i)
            return f_list
    return f_list


def sort_queue(queue):
    new_queue = Queue()
    new_list = []

    while not queue.empty():
        new_list.append(queue.get())
    # now new_list is the queue, sort new_list
    while len(new_list):
        temp_v = new_list[0]
        for i in range(len(new_list)):
            if temp_v[2] > new_list[i][2]:
                temp_v = new_list[i]
        # now temp_v is max
        new_queue.put(temp_v)
        new_list = Delete_position_in_list(new_list, temp_v)
    return new_queue


def ucs_algorithm(matrix, target_l, target_r, uer_stamina, W, H, start_l, start_r):
    current_value = matrix[start_r][start_l]
    min_value = []
    # Now find road to next
    # print(current_value, start_l, start_r)
    path = []
    current_l = start_l
    current_r = start_r
    position = 0

    temp_queue = Queue()

    path_map = np.zeros([H, W], int)

    start = [current_l, current_r, current_value, []]
    queue = Queue()
    appear = []

    adj_arr = []

    # make queue here
    queue.put(start)

    new_list = [[start_l, start_r, current_value, []]]
    final_target = []

    find_position_value = []
    while 1:
        adj_arr = []
        if queue.empty():
            return 'FAIL'
        current = queue.get()  # current [start_l, start_r]
        # print(current)
        current_l = current[0]
        current_r = current[1]
        current_value = matrix[current_r][current_l]
        if current_l == target_l and current_r == target_r:
            final_target = current
            break  # same as return current, but not go out function

        # Next we get the expanded children.
        if W > current_l >= 0 and H > current_r >= 0:
            # we are in the map now
            # test 8-directions
            if W > current_l - 1 >= 0 and H > current_r - 1 >= 0:
                # left up point
                if current_value > 0 and matrix[current_r - 1][current_l - 1] > 0 and current_value - matrix[current_r - 1][current_l - 1] >= 0:
                    adj_arr.append([current_l - 1, current_r - 1, 14, [current_l, current_r]])
                elif matrix[current_r - 1][current_l - 1] < 0 and abs(current_value) >= abs(matrix[current_r - 1][current_l - 1]):
                    adj_arr.append([current_l - 1, current_r - 1, 14, [current_l, current_r]])
                elif abs(current_value - matrix[current_r - 1][current_l - 1]) <= uer_stamina:
                    adj_arr.append([current_l - 1, current_r - 1, 14, [current_l, current_r]])

            if 0 <= current_r - 1 < H:
                # up point
                if current_value > 0 and matrix[current_r - 1][current_l] > 0 and current_value - matrix[current_r - 1][current_l] >= 0:
                    adj_arr.append([current_l, current_r - 1, 10, [current_l, current_r]])
                elif matrix[current_r - 1][current_l] < 0 and abs(current_value) >= abs(matrix[current_r - 1][current_l]):
                    adj_arr.append([current_l, current_r - 1, 10, [current_l, current_r]])
                elif abs(current_value - matrix[current_r - 1][current_l]) <= uer_stamina:
                    adj_arr.append([current_l, current_r - 1, 10, [current_l, current_r]])

            if H > current_r - 1 >= 0 and 0 <= current_l + 1 < W:
                # right up point
                if current_value > 0 and matrix[current_r - 1][current_l + 1] > 0 and current_value - matrix[current_r - 1][current_l + 1] >= 0:
                    adj_arr.append([current_l + 1, current_r - 1, 14, [current_l, current_r]])
                elif matrix[current_r - 1][current_l + 1] < 0 and abs(current_value) >= abs(
                        matrix[current_r - 1][current_l + 1]):
                    adj_arr.append([current_l + 1, current_r - 1, 14, [current_l, current_r]])
                elif abs(current_value - matrix[current_r - 1][current_l + 1]) <= uer_stamina:
                    adj_arr.append([current_l + 1, current_r - 1, 14, [current_l, current_r]])

            if 0 <= current_l + 1 < W:
                # right point
                if current_value > 0 and matrix[current_r][current_l + 1] > 0 and current_value -matrix[current_r][current_l + 1] >= 0:
                    adj_arr.append([current_l + 1, current_r, 10, [current_l, current_r]])
                elif matrix[current_r][current_l + 1] < 0 and abs(current_value) >= abs(matrix[current_r][current_l + 1]):
                    adj_arr.append([current_l + 1, current_r, 10, [current_l, current_r]])
                elif abs(current_value - matrix[current_r][current_l + 1]) <= uer_stamina:
                    adj_arr.append([current_l + 1, current_r, 10, [current_l, current_r]])

            if 0 <= current_l + 1 < W and 0 <= current_r + 1 < H:
                # right low point
                if current_value > 0 and matrix[current_r + 1][current_l + 1] > 0 and current_value - matrix[current_r + 1][current_l + 1] >= 0:
                    adj_arr.append([current_l + 1, current_r + 1, 14, [current_l, current_r]])
                elif matrix[current_r + 1][current_l + 1] < 0 and abs(current_value) >= abs(
                        matrix[current_r + 1][current_l + 1]):
                    adj_arr.append([current_l + 1, current_r + 1, 14, [current_l, current_r]])
                elif abs(current_value - matrix[current_r + 1][current_l + 1]) <= uer_stamina:
                    adj_arr.append([current_l + 1, current_r + 1, 14, [current_l, current_r]])

            if 0 <= current_l - 1 < W and H > current_r + 1 >= 0:
                # left low point
                if current_value > 0 and matrix[current_r + 1][current_l - 1] > 0 and current_value - matrix[current_r + 1][current_l - 1] >= 0:
                    adj_arr.append([current_l - 1, current_r + 1, 14, [current_l, current_r]])
                elif matrix[current_r + 1][current_l - 1] < 0 and abs(current_value) >= abs(
                        matrix[current_r + 1][current_l - 1]):
                    adj_arr.append([current_l - 1, current_r + 1, 14, [current_l, current_r]])
                elif abs(current_value - matrix[current_r + 1][current_l - 1]) <= uer_stamina:
                    adj_arr.append([current_l - 1, current_r + 1, 14, [current_l, current_r]])

            if 0 <= current_r + 1 < H and W > current_l >= 0:
                # low point
                if current_value > 0 and matrix[current_r + 1][current_l] > 0 and current_value - matrix[current_r + 1][current_l] >= 0:
                    adj_arr.append([current_l, current_r + 1, 10, [current_l, current_r]])
                elif matrix[current_r + 1][current_l] < 0 and abs(current_value) >= abs(matrix[current_r + 1][current_l]):
                    adj_arr.append([current_l, current_r + 1, 10, [current_l, current_r]])
                elif abs(current_value - matrix[current_r + 1][current_l]) <= uer_stamina:
                    adj_arr.append([current_l, current_r + 1, 10, [current_l, current_r]])

            if W > current_l - 1 >= 0 and H > current_r >= 0:
                # left point
                if current_value > 0 and matrix[current_r][current_l - 1] > 0 and current_value - matrix[current_r][current_l - 1] >= 0:
                    adj_arr.append([current_l - 1, current_r, 10, [current_l, current_r]])
                elif matrix[current_r][current_l - 1] < 0 and abs(current_value) >= abs(matrix[current_r][current_l - 1]):
                    adj_arr.append([current_l - 1, current_r, 10, [current_l, current_r]])
                elif abs(current_value - matrix[current_r][current_l - 1]) <= uer_stamina:
                    adj_arr.append([current_l - 1, current_r, 10, [current_l, current_r]])
        else:
            return 'FAIL'

        # print(f'This is the list after expanded node', adj_arr)
        # Now we get all the children that expanded
        while len(adj_arr):
            # print('-------------------------------')
            # print(f'This is the adj_arr', adj_arr)
            current_child = adj_arr[0]
            adj_arr.pop(0)
            # print(f'This is the list after one remove node', adj_arr)

            # now dealing with node operation
            [queue, find_position_value] = find_position_in_queue(queue, current_child)
            appear_position_value = find_position_in_list(appear, current_child)
            if not find_position_value and not appear_position_value:
                current_child[2] = current[2] + current_child[2]
                # print(f'This is the current node after add', current_child)
                new_list.append(current_child)
                # print(f'We put current to queue for case 1', current_child)
                queue.put(current_child)
                # print(f'This is the queue for one step', queue.qsize())
            elif find_position_value:
                node_cost = find_position_value
                # print(f'This is the node_cost', node_cost)
                cost = current_child[2] = current[2] + current_child[2]
                if cost < node_cost[2]:
                    queue = Delete_position_in_queue(queue, node_cost)
                    # print(f'This is the Queue after delete cost', queue)
                    new_list = Delete_position_in_list(new_list, node_cost)
                    new_list.append(current_child)
                    # print(f'We put current to queue for case 2', current_child)
                    queue.put(current_child)
            elif appear_position_value:
                node_cost = find_position_in_list(appear, current_child)  # node_cost is [x, y, value, [x, y]]
                cost = current_child[2] = current[2] + current_child[2]
                if cost < node_cost[2]:
                    appear = Delete_position_in_list(appear, node_cost)
                    # print(f'This is the list after delete cost', list)
                    new_list = Delete_position_in_list(new_list, node_cost)
                    new_list.append(current_child)
                    # print(f'We put current to queue for case 3', current_child)
                    queue.put(current_child)
            # print('----------------------------------------')
        # print(f'This is the queue before sort', queue.qsize())
        appear.append(current)
        queue = sort_queue(queue)
        # print(f'This is the queue after sort', queue.qsize())
        # print(f'This is the new_list', new_list)
    # print(f'This is the new_list', new_list)

    for i in range(len(new_list)):
        if target_l == new_list[i][0] and target_r == new_list[i][1]:
            position = i

    back_parent = new_list[position]
    while back_parent[0] != start_l or back_parent[1] != start_r:
        # print(f'This is the back', back_parent)
        parent = back_parent[3]
        # print(f'this is the small parent', parent)
        path.append([back_parent[0], back_parent[1]])
        # we find the parent
        for i in range(len(new_list)):
            if parent[0] == new_list[i][0] and parent[1] == new_list[i][1]:
                position = i

        # print(f'This is the parent', new_list[position])
        back_parent = new_list[position]
        # print(f'This is the back_parent', back_parent)
    path.append([start_l, start_r])
    # print(f'This is the path', path)
    return path


def ucs_method(matrix, target_point_list, target_point_num, uer_stamina, W, H, start_l, start_r):
    count_p = 0
    if target_point_num == 1:
        target_l = target_point_list[0]
        target_r = target_point_list[1]
        path = ucs_algorithm(matrix, target_l, target_r, uer_stamina, W, H, start_l, start_r)
        count_p = write_txt(path, target_point_num, count_p)
    else:
        for k in range(target_point_num):
            target_current = target_point_list[k]
            target_l = target_current[0]
            target_r = target_current[1]
            path = ucs_algorithm(matrix, target_l, target_r, uer_stamina, W, H, start_l, start_r)
            count_p = write_txt(path, target_point_num, count_p)


def get_momentum(E_p, E_c, E_n):
    output_v = 0
    if E_n - E_c > 0:
        output_v = max(0, E_p - E_c)
    elif E_n - E_c <= 0:
        output_v = 0
    return 0


def get_path_cost(E_p, E_c, E_n, M):
    ECCost = 0
    if E_n - E_c <= M:
        ECCost = 0
    elif E_n-E_c > M:
        ECCost = max(0, E_n-E_c-M)
    return ECCost


def evaluation_f_for_A(target_l, target_r, current_l, current_r):
    manhattan_v = abs(target_r - current_r) + abs(target_l - current_l)
    return manhattan_v


def A_algorithm(matrix, target_l, target_r, uer_stamina, W, H, start_l, start_r):
    current_value = matrix[start_r][start_l]
    min_value = []
    # Now find road to next
    path = []
    current_l = start_l
    current_r = start_r
    position = 0

    temp_queue = Queue()

    path_map = np.zeros([H, W], int)

    start = [current_l, current_r, matrix[current_r][current_l], []]
    queue = Queue()
    appear = []

    adj_arr = []

    # make queue here
    queue.put(start)

    new_list = [[start_l, start_r, matrix[current_r][current_l], []]]
    final_target = []

    find_position_value = []
    prev_M = 0
    prev_Cost = 0
    while 1:
        adj_arr = []
        if queue.empty():
            return 'FAIL'
        current = queue.get()  # current [start_l, start_r]
        current_l = current[0]
        current_r = current[1]
        if current_l == target_l and current_r == target_r:
            final_target = current
            break  # same as return current, but not go out function
        # Next we get the expanded children.
        if W > current_l >= 0 and H > current_r >= 0:
            # we are in the map now
            # test 8-directions
            if W > current_l - 1 >= 0 and H > current_r - 1 >= 0:
                # left up point
                M = get_momentum(prev_M, matrix[current_r][current_l], matrix[current_r - 1][current_l - 1])
                c_cost = get_path_cost(prev_M, current[2], matrix[current_r - 1][current_l - 1], M)
                if current_value > 0 and matrix[current_r - 1][current_l - 1] > 0 and current_value - matrix[current_r - 1][current_l - 1] >= 0:
                    adj_arr.append([current_l - 1, current_r - 1, 14 + c_cost, [current_l, current_r]])
                elif matrix[current_r - 1][current_l - 1] < 0 and abs(current_value) >= abs(matrix[current_r - 1][current_l - 1]):
                    adj_arr.append([current_l - 1, current_r - 1, 14 + c_cost, [current_l, current_r]])
                elif abs(current_value - matrix[current_r - 1][current_l - 1]) - M <= uer_stamina:
                    adj_arr.append([current_l - 1, current_r - 1, 14 + c_cost, [current_l, current_r]])

            if 0 <= current_r - 1 < H:
                # up point
                M = get_momentum(prev_M, matrix[current_r][current_l], matrix[current_r - 1][current_l])
                c_cost = get_path_cost(prev_M, current[2], matrix[current_r - 1][current_l], M)
                if current_value > 0 and matrix[current_r - 1][current_l] > 0 and current_value - matrix[current_r - 1][current_l] >= 0:
                    adj_arr.append([current_l, current_r - 1, 10 + c_cost, [current_l, current_r]])
                elif matrix[current_r - 1][current_l] < 0 and abs(current_value) >= abs(matrix[current_r - 1][current_l]):
                    adj_arr.append([current_l, current_r - 1, 10 + c_cost, [current_l, current_r]])
                elif abs(current_value - matrix[current_r - 1][current_l]) - M <= uer_stamina:
                    adj_arr.append([current_l, current_r - 1, 10 + c_cost, [current_l, current_r]])

            if H > current_r - 1 >= 0 and 0 <= current_l + 1 < W:
                # right up point
                M = get_momentum(prev_M, matrix[current_r][current_l], matrix[current_r - 1][current_l + 1])
                c_cost = get_path_cost(prev_M, current[2], matrix[current_r - 1][current_l + 1], M)
                if current_value > 0 and matrix[current_r - 1][current_l + 1] > 0 and current_value - matrix[current_r - 1][current_l + 1] >= 0:
                    adj_arr.append([current_l + 1, current_r - 1, 14 + c_cost, [current_l, current_r]])
                elif matrix[current_r - 1][current_l + 1] < 0 and abs(current_value) >= abs(matrix[current_r - 1][current_l + 1]):
                    adj_arr.append([current_l + 1, current_r - 1, 14 + c_cost, [current_l, current_r]])
                elif abs(current_value - matrix[current_r - 1][current_l + 1]) <= uer_stamina:
                    adj_arr.append([current_l + 1, current_r - 1, 14 + c_cost, [current_l, current_r]])

            if 0 <= current_l + 1 < W:
                # right point
                M = get_momentum(prev_M, matrix[current_r][current_l], matrix[current_r][current_l + 1])
                c_cost = get_path_cost(prev_M, current[2], matrix[current_r][current_l + 1], M)
                if current_value > 0 and matrix[current_r][current_l + 1] > 0 and current_value - matrix[current_r][current_l + 1] >= 0:
                    adj_arr.append([current_l + 1, current_r, 10 + c_cost, [current_l, current_r]])
                elif matrix[current_r][current_l + 1] < 0 and abs(current_value) >= abs(matrix[current_r][current_l + 1]):
                    adj_arr.append([current_l + 1, current_r, 10 + c_cost, [current_l, current_r]])
                elif abs(current_value - matrix[current_r][current_l + 1]) <= uer_stamina:
                    adj_arr.append([current_l + 1, current_r, 10 + c_cost, [current_l, current_r]])

            if 0 <= current_l + 1 < W and 0 <= current_r + 1 < H:
                # right low point
                M = get_momentum(prev_M, matrix[current_r][current_l], matrix[current_r + 1][current_l + 1])
                c_cost = get_path_cost(prev_M, current[2], matrix[current_r + 1][current_l + 1], M)
                if current_value > 0 and matrix[current_r + 1][current_l + 1] > 0 and current_value - matrix[current_r + 1][current_l + 1] >= 0:
                    adj_arr.append([current_l + 1, current_r + 1, 14 + c_cost, [current_l, current_r]])
                elif matrix[current_r + 1][current_l + 1] < 0 and abs(current_value) >= abs(matrix[current_r + 1][current_l + 1]):
                    adj_arr.append([current_l + 1, current_r + 1, 14 + c_cost, [current_l, current_r]])
                elif abs(current_value - matrix[current_r + 1][current_l + 1]) <= uer_stamina:
                    adj_arr.append([current_l + 1, current_r + 1, 14 + c_cost, [current_l, current_r]])

            if 0 <= current_l - 1 < W and H > current_r + 1 >= 0:
                # left low point
                M = get_momentum(prev_M, matrix[current_r][current_l], matrix[current_r + 1][current_l - 1])
                c_cost = get_path_cost(prev_M, current[2], matrix[current_r + 1][current_l - 1], M)
                if current_value > 0 and matrix[current_r + 1][current_l - 1] > 0 and current_value - matrix[current_r + 1][current_l - 1] >= 0:
                    adj_arr.append([current_l - 1, current_r + 1, 14 + c_cost, [current_l, current_r]])
                elif matrix[current_r + 1][current_l - 1] < 0 and abs(current_value) >= abs(matrix[current_r + 1][current_l - 1]):
                    adj_arr.append([current_l - 1, current_r + 1, 14 + c_cost, [current_l, current_r]])
                elif abs(current_value - matrix[current_r + 1][current_l - 1]) <= uer_stamina:
                    adj_arr.append([current_l - 1, current_r + 1, 14 + c_cost, [current_l, current_r]])

            if 0 <= current_r + 1 < H and W > current_l >= 0:
                # low point
                M = get_momentum(prev_M, matrix[current_r][current_l], matrix[current_r + 1][current_l])
                c_cost = get_path_cost(prev_M, current[2], matrix[current_r + 1][current_l], M)
                if current_value > 0 and matrix[current_r + 1][current_l] > 0 and current_value - matrix[current_r + 1][current_l] >= 0:
                    adj_arr.append([current_l, current_r + 1, 10 + c_cost, [current_l, current_r]])
                elif matrix[current_r + 1][current_l] < 0 and abs(current_value) >= abs(matrix[current_r + 1][current_l]):
                    adj_arr.append([current_l, current_r + 1, 10 + c_cost, [current_l, current_r]])
                elif abs(current_value - matrix[current_r + 1][current_l]) <= uer_stamina:
                    adj_arr.append([current_l, current_r + 1, 10 + c_cost, [current_l, current_r]])

            if W > current_l - 1 >= 0 and H > current_r >= 0:
                # left point
                M = get_momentum(prev_M, matrix[current_r][current_l], matrix[current_r][current_l - 1])
                c_cost = get_path_cost(prev_M, current[2], matrix[current_r][current_l - 1], M)
                if current_value > 0 and matrix[current_r][current_l - 1] > 0 and current_value - matrix[current_r][current_l - 1] >= 0:
                    adj_arr.append([current_l - 1, current_r, 10 + c_cost, [current_l, current_r]])
                elif matrix[current_r][current_l - 1] < 0 and abs(current_value) >= abs(matrix[current_r][current_l - 1]):
                    adj_arr.append([current_l - 1, current_r, 10 + c_cost, [current_l, current_r]])
                elif abs(current_value - matrix[current_r][current_l - 1]) <= uer_stamina:
                    adj_arr.append([current_l - 1, current_r, 10 + c_cost, [current_l, current_r]])
        else:
            return 'FAIL'

        # print(f'This is the list after expanded node', adj_arr)
        # Now we get all the children that expanded
        while len(adj_arr):
            # print(f'This is the adj_arr', adj_arr)
            current_child = adj_arr[0]
            adj_arr.pop(0)
            # print(f'This is the list after one remove node', adj_arr)

            # now dealing with node operation
            [queue, find_position_value] = find_position_in_queue(queue, current_child)
            appear_position_value = find_position_in_list(appear, current_child)
            if not find_position_value and not appear_position_value:
                current_child[2] = current[2] + current_child[2] + evaluation_f_for_A(target_l, target_r, current_child[0], current_child[1])
                new_list.append(current_child)
                queue.put(current_child)
            elif find_position_value:
                node_cost = find_position_value
                cost = current_child[2] = current[2] + current_child[2] + evaluation_f_for_A(target_l, target_r, current_child[0], current_child[1])
                if cost < node_cost[2]:
                    queue = Delete_position_in_queue(queue, node_cost)
                    new_list = Delete_position_in_list(new_list, node_cost)
                    new_list.append(current_child)
                    queue.put(current_child)
            elif appear_position_value:
                continue
        prev_M = current[2]
        appear.append(current)
        queue = sort_queue(queue)

    # search finished
    for i in range(len(new_list)):
        if target_l == new_list[i][0] and target_r == new_list[i][1]:
            position = i

    back_parent = new_list[position]
    while back_parent[0] != start_l or back_parent[1] != start_r:
        parent = back_parent[3]
        path.append([back_parent[0], back_parent[1]])
        # we find the parent
        for i in range(len(new_list)):
            if parent[0] == new_list[i][0] and parent[1] == new_list[i][1]:
                position = i

        back_parent = new_list[position]

    path.append([start_l, start_r])
    # print(f'This is the path', path)
    return path


def A_method(matrix, target_point_list, target_point_num, uer_stamina, W, H, start_l, start_r):
    count_p = 0
    if target_point_num == 1:
        # print(f'this is list', target_point_list)
        target_l = target_point_list[0]
        target_r = target_point_list[1]
        # print(target_l, target_r)
        path = A_algorithm(matrix, target_l, target_r, uer_stamina, W, H, start_l, start_r)
        count_p = write_txt(path, target_point_num, count_p)
    else:
        for k in range(target_point_num):
            target_current = target_point_list[k]
            target_l = target_current[0]
            target_r = target_current[1]
            path = A_algorithm(matrix, target_l, target_r, uer_stamina, W, H, start_l, start_r)
            count_p = write_txt(path, target_point_num, count_p)


if __name__ == '__main__':
    t_matrix = open_txt('./')
    t_matrix = matrix_trans(t_matrix)
    # Dealing with parameters
    method = t_matrix[0]

    HW_matrix = matrix_further_trans(t_matrix[1][0])
    W = int(HW_matrix[0])
    H = int(HW_matrix[1])

    start_matrix = matrix_further_trans(t_matrix[2][0])
    start_left = int(start_matrix[0])
    start_right = int(start_matrix[1])

    stamina = matrix_further_trans(t_matrix[3][0])
    stamina = int(stamina[0])

    lodges_num = matrix_further_trans(t_matrix[4][0])
    lodges_num = int(lodges_num[0])

    if lodges_num - 1 == 0:
        temp = t_matrix[5][0]
        temp = temp.strip('').split()
        for j in range(2):
            temp[j] = int(temp[j])
        temp = np.array(temp)
        temp_reshape = temp.reshape(2)

        final_matrix = temp_reshape
    else:
        for i in range(0, lodges_num):
            if i == 0:
                temp = t_matrix[5][0]
                temp = temp.strip('').split()
                for j in range(2):
                    temp[j] = int(temp[j])
                temp = np.array(temp)
                temp_reshape = temp.reshape(2)

                final_matrix = temp_reshape
            else:
                temp = t_matrix[i + 5][0]
                temp = temp.strip('').split()
                for j in range(2):
                    temp[j] = int(temp[j])
                temp = np.array(temp)
                temp_reshape = temp.reshape(2)
                final_matrix = np.row_stack((final_matrix, temp_reshape))

    lodges_pointlist = final_matrix
    # print(f'This is lodges_pointlist', lodges_pointlist)

    for i in range(H):
        if i == 0:
            temp = t_matrix[i + 5 + lodges_num][0]
            temp = temp.strip('').split()
            for j in range(W):
                temp[j] = int(temp[j])
            temp = np.array(temp)
            temp_reshape = temp.reshape(W)

            final_matrix = temp_reshape
        else:
            temp = t_matrix[i + 5 + lodges_num][0]
            temp = temp.strip('').split()
            for j in range(W):
                temp[j] = int(temp[j])
            temp = np.array(temp)
            temp_reshape = temp.reshape(W)

            final_matrix = np.row_stack((final_matrix, temp_reshape))
    # print(f'This is final_matrix\n', final_matrix)
    # Data preprocessing finished, then do algorithm

    if method[0] == 'BFS':
        bfs_method(final_matrix, lodges_pointlist, lodges_num, stamina, W, H, start_left, start_right)
    elif method[0] == 'UCS':
        ucs_method(final_matrix, lodges_pointlist, lodges_num, stamina, W, H, start_left, start_right)
    elif method[0] == 'A*':
        A_method(final_matrix, lodges_pointlist, lodges_num, stamina, W, H, start_left, start_right)
