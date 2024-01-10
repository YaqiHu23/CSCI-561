import datetime
import numpy as np
import os


def write_txt(computer_runtime):
    if os.path.isfile('calibrate.txt'):
        os.remove('calibrate.txt')
    txt_name = 'calibrate.txt'

    computer_runtime = str(computer_runtime)
    with open(txt_name, 'a') as file:
        file.write(computer_runtime)


time = np.zeros(2)
for i in range(2):
    start_time = datetime.datetime.now()
    for j in range(10):
        a = np.ones([10000, 10500], dtype=float)
        b = np.ones([10500, 11000], dtype=float)
        np.matmul(a, b)
    end_time = datetime.datetime.now()

    time[i] = (end_time - start_time).total_seconds()

    final_time = (time[0] + time[1]) / 2

    write_txt(int(final_time))
