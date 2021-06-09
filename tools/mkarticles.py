# hello.py - http://www.graphviz.org/content/hello
# -*- coding: utf-8 -*-

x = range(2,201)
for i in x:
    name = 'nw_' + str(i) + '.md'
    text = '**--' + str(i) + '--**\n\n' + 'Здесь еще нет информации\n\n' + 'Ссылки:'
    f = open(name, "w")
    f.write(text)
    f.close()
for i in x:
    name = 'pw_' + str(i) + '.md'
    text = '**++' + str(i) + '++**\n\n' + 'Здесь еще нет информации\n\n' + 'Ссылки:'
    f = open(name, "w")
    f.write(text)
    f.close()

