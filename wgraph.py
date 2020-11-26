# hello.py - http://www.graphviz.org/content/hello
# -*- coding: utf-8 -*-

import re
import sys
import yaml
import format
from graphviz import Digraph


## Graph creation
def wgraph(yaml_data, status_dict, graph_file):

    g = Digraph('G', filename=graph_file, format='svg')
    #g = Digraph('G', filename=graph_file)


    for record in yaml_data['statements']:
        m1 = re.match('\+', record['wave'])
        m2 = re.match('-', record['wave'])
        if m1:
            lbl = record['id'] + '\n' + format.format(record['text'])
            if not (record['id'] in status_dict.keys()):
                g.attr('node', color='red', fontcolor = 'black')
                g.node(record['id'], label=lbl, URL='https://www.ru')
            else:
                g.attr('node', color='gray90', fontcolor = 'gray90')
                g.node(record['id'], label=lbl, URL='https://www.ru')

        elif m2:
            lbl = record['id'] + '\n' + format.format(record['text'])
            if not (record['id'] in status_dict.keys()): 
                g.attr('node', color='blue', href='https://www.ru',  fontcolor = 'black')
                g.node(record['id'], label=lbl)
            else:
                g.attr('node', color='gray90', fontcolor = 'gray90')
                g.node(record['id'], label=lbl, URL='https://www.ru')

    ### Edge creation

    for record in yaml_data['statements']:
        for edge in record['direct_contradictions']:
            if edge['id']:
                if not (edge['id'] in status_dict.keys()):
                    g.edge(record['id'], edge['id'])
                else:
                    g.edge(record['id'], edge['id'], color='gray90')
        for edge in record['indirect_contradictions']:
            if edge['id']:
                if not (edge['id'] in status_dict.keys()):
                    g.edge(record['id'], edge['id'], style='dotted')
                else:
                    g.edge(record['id'], edge['id'], color='gray90',style='dotted')
        for edge in record['complement']:
            if edge['id']:
                if not (edge['id'] in status_dict.keys()):
                    g.edge(record['id'], edge['id'], color='red', dir="both")
                else:
                    g.edge(record['id'], edge['id'], color='gray90', dir="both")

    g.render(view=False)  
#   g.view()

if __name__ == "__main__":

    ######### get file's names from the command line ####################
    if (len(sys.argv)==3):
        yaml_file = sys.argv[1]
        graph_file = sys.argv[2]
    else:
        print ("   ######################################################\n")
        print ("   Syntax is:\n")
        print ("   python3 ../../wgraph.py desdemona.yml desdemona.gv\n")
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

    wgraph(yaml_data, {}, graph_file)
