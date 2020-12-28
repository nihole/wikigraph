import math
import re

def format(string, x=3, y=1):
# format text: height (lines)/width(symbols) = y/x (approximately)
    str_len = len(string)
    # calculate width in symbols 
    width = math.floor (math.sqrt (str_len * x / y))
    # height in lines
    height = math.floor (math.sqrt(str_len * y / x))

    words_list = re.split("[\s]", string)
    l = 0
    str_list = []
    str_ = ''
    len_ = len(words_list)
    for i, wd in enumerate(words_list):
        if l == 0:
            str_ =  wd
            l += len(wd)
        elif l > 0 and l < width:
            str_ += ' ' + wd
            l += len(wd)
        if (l >= width) or (len_ == i + 1):
            str_list.append(str_)
            l = 0
            str_ = ''
    new_str = '\n'.join(str_list)
    return new_str

