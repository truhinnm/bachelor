from pyconfig import *


def get_params_list(some_list):
    new_list = []
    for param in some_list:
        if param[1] == 1:
            new_list.append(param[0])
    return new_list
