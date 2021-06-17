# hello.py - http://www.graphviz.org/content/hello
# -*- coding: utf-8 -*-

###################################################################
#                                                                 #
#    Extracts a sub-wikigraph with a particular node as root      #
#                                                                 #
##################################################################

import sys
import re
import yaml

def search_node (node_id):
    global parent_yaml_data
    flag = 0
    for node in parent_yaml_data['statements']:
        if node['id'] == node_id:
            flag = 1
            print (node_id)
            break
    if flag == 1:
        return node
    else:
        quit("Error!! Node with id %s does not extits!!" % node_id)

def get_downstreem_nodes(node):
    ds_node_ids = []
    for el in node['direct_contradictions']:
        if el:
            ds_node_ids.append(el['id'])
    for el in node['indirect_contradictions']:
        if el:
            ds_node_ids.append(el['id'])
    for el in node['complement']:
        if el:
            ds_node_ids.append(el['id'])
    ds_node_ids = list(set(ds_node_ids))
    return ds_node_ids

def add_node(node_id):
    global new_yaml_data
    global nodes
    global new_node_ids
    new_node = search_node(node_id)
    nodes.append(new_node.copy())
    ds_node_ids = get_downstreem_nodes(new_node)
    for id_ in ds_node_ids:
         if not id_ in new_node_ids:
             new_node_ids.append(id_)


######### get file's names from the command line ####################

if (len(sys.argv)==4):
    yaml_file = sys.argv[1]
    new_yaml_file = sys.argv[2]
    node_id = sys.argv[3]
    print (node_id)
else:
    print ("   ######################################################\n")
    print ("   Syntax is:\n")
    print ("   python extract.py parent_wikigraph.yml sub_wikigraph.yml node_id \n")
    print ("   ######################################################\n")
    quit()


   ######### take data from parent YAML file ####################

f = open( "%s" % yaml_file )
data1 = f.read()
f.close()

yaml_version = yaml.__version__
m = re.match('(\d(\.\d)?)', yaml_version)
yaml_ver = m.group(1)

if (float(yaml_ver) < 5.1):
   paernt_yaml_data = yaml.load(data1)
else:
    parent_yaml_data = yaml.load(data1,Loader=yaml.FullLoader)

######### creation a child YAML file ###################

nodes = []
new_node_ids=[]
new_yaml_data = {'statements':nodes}

add_node(node_id)
for node_id in new_node_ids:
    if node_id:
        add_node(node_id)
    

print (new_node_ids)


with open(new_yaml_file, 'w') as yaml_file:
    yaml.dump(new_yaml_data, yaml_file, default_flow_style=False, sort_keys=False) 
       
