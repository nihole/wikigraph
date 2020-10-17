# hello.py - http://www.graphviz.org/content/hello
# -*- coding: utf-8 -*-

import format
from graphviz import Digraph

label_list = []
label_list.append("+++ 0 +++\n" + format.format("Дездемона изменила Отелло").decode('utf-8'))
label_list.append("+++ 1 +++\n" + format.format("Дездемона не\nизменяла Отелло").decode('utf-8'))

g = Digraph('G', filename='Desdemona.gv')
g.attr('node', color='red')
g.node('0', label = label_list[0])
g.attr('node', color='blue')
g.node('1', label = label_list[1])
g.edge('0', '1')

g.view()
