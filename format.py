import math
import re

def format(string, x=3, y=1):
    str_len = len(string)
    width = math.floor (math.sqrt (str_len * x / y))
    height = math.floor (math.sqrt(str_len * y / x))
    words_list = re.split("[\s\n]", string)
    l = 0
    str_list = []
    str_ = ''
    for wd in words_list:
        if l > 0:
            str_ += ' ' + wd
        else:
            str_ =  wd
        l += len(wd)
        if l >= width:
            str_list.append(str_)
            l = 0
            str_ = ''
    new_str = '\n'.join(str_list)
    return new_str



            




