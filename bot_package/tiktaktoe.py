import numpy as np

from . import utils

NEXTLINE = '\n'

IndexDict = {
    7: 0,
    8: 1,
    9: 2,
    4: 3,
    5: 4,
    6: 5,
    1: 6,
    2: 7,
    3: 8,
    "board": "........."
}


def ttt():
    n = '3'
    print("debug_out: " + n + " Felder")
    print(IndexDict["board"])
    args = ['./driver/ALGODAT_A04_HA.jar', n, '1', '1', '1', IndexDict["board"]]
    result = utils.jarwrapper(*args)
    print(result)
    IndexDict["board"] = result[1].strip(str.encode('\r')).decode()
    print(IndexDict["board"])

    return (result[0] + NEXTLINE.encode()).decode()


def string_to_board(los):
    temp_n = int(len(los) ** 0.5)
    temp = np.asarray(list(los)).reshape(temp_n, temp_n)
    ret_s = ''
    for i in range(temp_n):
        for j in range(temp_n):
            ret_s += temp[i][j] + '     '
        ret_s += '\n'
    return ret_s
