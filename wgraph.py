# hello.py - http://www.graphviz.org/content/hello
# -*- coding: utf-8 -*-

import re
import sys
import yaml
import format
import wlib
from graphviz import Digraph


## Graph creation
def wgraph(yaml_data, status_dict, phase, graph_file):

    g = Digraph('G', filename=graph_file, format='svg')
    #g = Digraph('G', filename=graph_file)


    for record in yaml_data['statements']:
#        m1 = re.match('\+', record['wave'])
#        m2 = re.match('-', record['wave'])
        if phase[record['id']]:
            lbl = record['id'] + '\n' + format.format(record['text'])
            if not (record['id'] in status_dict.keys()):
                g.attr('node', color='red', href=record['wiki_link'], fontcolor = 'black')
                g.node(record['id'], label=lbl)
            else:
                g.attr('node', color='gray90', href=record['wiki_link'], fontcolor = 'gray90')
                g.node(record['id'], label=lbl)

        else:
            lbl = record['id'] + '\n' + format.format(record['text'])
            if not (record['id'] in status_dict.keys()): 
                g.attr('node', color='blue', href=record['wiki_link'],  fontcolor = 'black')
                g.node(record['id'], label=lbl)
            else:
                g.attr('node', color='gray90', href=record['wiki_link'], fontcolor = 'gray90')
                g.node(record['id'], label=lbl)

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
        print ("   python3 ../wikigraph/wgraph.py yaml/desdemona.yml desdemona\n")
        print ("   ######################################################\n")
        quit()


   ######### take data from YAML file ####################

    my_config=''
    f = open( "%s" % yaml_file, encoding='utf-8')
    data1 = f.read()
    f.close()

    (root_id, rdict, reverse_rdict, phase,  paths_dict ) = wlib.check_structure(yaml_data)

    wgraph(yaml_data, {}, phase, graph_file)
