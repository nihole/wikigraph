# hello.py - http://www.graphviz.org/content/hello
# -*- coding: utf-8 -*-

import re
import sys
import yaml
import format
from graphviz import Digraph

    ######### get file's names from the command line ####################
if (len(sys.argv)==3):
    yaml_file = sys.argv[1]
    graph_file = sys.argv[2]
else:
    print ("   ######################################################\n")
    print ("   Syntax is:\n")
    print ("   python3 ../../gcreator.py desdemona.yml desdemona.gv\n")
    print ("   ######################################################\n")
    quit()


   ######### take data from YAML file ####################
my_config=''
f = open( "%s" % yaml_file )
data1 = f.read()
f.close()

yaml_version = yaml.__version__
m = re.match('(\d(\.\d)?)', yaml_version)
yaml_ver = m.group(1)

if (float(yaml_ver) < 5.1):
    yaml_data = yaml.load(data1)
else:
    yaml_data = yaml.load(data1,Loader=yaml.FullLoader)

## Graph creation



#label_list = []
#label_list.append("+++ 0 +++\n" + format.format("Дездемона изменила Отелло").decode('utf-8'))
#label_list.append("+++ 1 +++\n" + format.format("Дездемона не\nизменяла Отелло").decode('utf-8'))

g = Digraph('G', filename=graph_file)

for record in yaml_data['statements']:
    m1 = re.match('\+', record['wave'])
    m2 = re.match('-', record['wave'])
    if m1:
        g.attr('node', color='red')
        g.node(record['id'], label = format.format(record['text']))
    elif m2:
        g.attr('node', color='blue')
        g.node(record['id'], label = format.format(record['text']))
    else:
        g.attr('node', color='none')
        g.node(record['id'], label = format.format(record['text']))

### Edge creation

for record in yaml_data['statements']:
    for edge in record['direct_contradictions']:
        if edge['id']:
            g.edge(record['id'], edge['id'])
    for edge in record['indirect_contradictions']:
        if edge['id']:
            g.edge(record['id'], edge['id'], style='dotted')
    for edge in record['complement']:
        if edge['id']:
#            g.attr['edge',  color='red']
            g.edge(record['id'], edge['id'], color='red', dir="both")

g.view()
