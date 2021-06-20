# hello.py - http://www.graphviz.org/content/hello
# -*- coding: utf-8 -*-

###################################################################
#                                                                 #
#    Extracts a sub-wikigraph with a particular node as root      #
#                                                                 #
##################################################################


'''

def search_node (yaml_data, node_id) 	- returns node (dictionary) with node['id'] == node_id
def get_downstreem_nodes(node) 		- for the node returns all downstream node's id as a list ds_node_ids
def extract_src_node_ids(node_id)	- finds all node IDs one step downstream of the node with the given node id in src_yaml_data and adds them to the global list source_node_ids 
def extract_dst_node_ids(node_id)       - finds all node IDs one step downstream of the node with the given node id in dst_yaml_data and adds them to the global list destination_node_ids
def check_upstream(node_id, yaml_data)	- finds and returns all node IDs one step upstream of the node with the given node id in yaml_data
def get_source_node_ids (node_id)	- creates a full list of node ids in waves starting with node_id taken from source file
def get_destination_node_ids (node_id)  - creates a full list of node ids in waves starting with node_id taken from destination file

'''

import sys
import re
import yaml
import getopt
import os
sys.path.insert(1,'../')
import wlib


### Displays the message requiring confirmation if merge or rewright is performed

def input_check(node_id, src_file, dst_file, merge):

    if merge:
        consent = input("\n  All waves having the root %s from file %s will be merged into %s\n  If you want to rewrite (not to merge) use this command without -m key.\n\n  MERGE (y|n)? " % (node_id, src_file, dst_file))
        if ((consent == 'y') or (consent == 'yes') or (consent == 'Y') or (consent == 'Yes') or (consent == '')):
           pass
        elif  (consent == 'n' or consent == 'no' or consent == 'N' or consent == 'No'):
            sys.xit ()
        else:
            sys.exit("  Incorrect input!!! Please use 'n' or press Enter")
    else:
        consent = input("\n  All waves having the root %s from file %s will rewrite all waves with a root in %s in %s\n  If you want to merge (to rewrite) use this command with -m key.\n\n  REWRITE (y|n)? " % (node_id, src_file, node_id, dst_file))
        if ((consent == 'y') or (consent == 'yes') or (consent == 'Y') or (consent == 'Yes') or (consent == '')):
            pass
        elif  (consent == 'n' or consent == 'no' or consent == 'n|N|y|Y|No|no|Yes|yes' or consent == 'No'):
            sys.exit ()
        else:
            sys.exit("  Incorrect input!!! Please use 'n|N|y|Y|No|no|Yes|yes' or press Enter")          

def usage_incorrect ():
  print('\nIncorrect syntax\nType python3 wgmerge.py -h')


### Help message

def help_info():
  print ("\n")
  print("##################################################################################################################################")
  print("#                                                                                                                                #")
  print("#  python -u wgmerge.py [ -h] -s src_file_name -d udst_file_name -n node_id [ -m]                                                #")
  print("#                                                                                                                                #")
  print("#  -s | --src_file src_file_name    - source file from which configuration is taken   					          #")
  print("#  -d | --dst_file dst_file_name    - destination file to which configuration is migrate                                         #")     
  print("#  -n | --node_id  node_id          - node id for migration                                                                      #")
  print("#  -m | --merge                     - merge (to add new and not change existing). Without this key everything is re-wrighted     #")
  print("#  -h | --help                      - help                                                                                       #")
  print("#                                                                                                                                #")
  print("#  Example: python -u wgmerge.py -s example4.yml -d nw_1 -n --1--  -m                                                            #")
  print("#                                                                                                                                #")
  print("##################################################################################################################################")
  print ("\n")

### Return nodes (dictionary) with node['id'] == node_id

def search_node (yaml_data, node_id):
    flag = 0
    for node in yaml_data['statements']:
        if node['id'] == node_id:
            flag = 1
            break
    if flag == 1:
        return node
    else:
        quit("Error!! Node with id %s does not extits!!" % node_id)

### For the node returns all downstream node's id as a list ds_node_ids

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

### Finds all node IDs one step downstream of the node with the given node id in src_yaml_data and adds them to the global list source_node_ids 

def extract_src_node_ids(node_id):
    global nodes
    global srs_yaml_data
    global source_node_ids
    new_node = search_node(src_yaml_data, node_id)
#    nodes.append(new_node.copy())
    ds_node_ids = get_downstreem_nodes(new_node)
    for id_ in ds_node_ids:
         if not id_ in source_node_ids:
             source_node_ids.append(id_)

### Finds all node IDs one step downstream of the node with the given node id in dst_yaml_data and adds them to the global list destination_node_ids

def extract_dst_node_ids(node_id):
    global nodes
    global dst_yaml_data
    global destination_node_ids
    new_node = search_node(dst_yaml_data, node_id)
#    nodes.append(new_node.copy())
    ds_node_ids = get_downstreem_nodes(new_node)
    for id_ in ds_node_ids:
         if not id_ in destination_node_ids:
             destination_node_ids.append(id_)

### Verufy if the node with node_id has upstread outside of source_node_ids. 
### If all upstream nodes are in source_node_ids and merge = False this node will be removed

def check_upstream(node_id, yaml_data):
    rec_yaml_data = {}
    rec_yaml_data = wlib.recurs_dict(yaml_data)
    reverse_node_ids = rec_yaml_data[0][node_id]['direct'] + rec_yaml_data[0][node_id]['indirect'] + rec_yaml_data[0][node_id]['complement']
    return (reverse_node_ids)

#def merge ():
    
    

### Creates a full list of node ids in waves starting with node_id taken from source file

def get_source_node_ids (node_id):
    global source_node_ids
    extract_src_node_ids(node_id)
    for node_id in source_node_ids:
        if node_id:
            extract_src_node_ids(node_id)
    if None in source_node_ids: source_node_ids.remove(None)
    if '' in source_node_ids: source_node_ids.remove('')

### Creates a full list of node ids in waves starting with node_id taken from destination file

def get_destination_node_ids (node_id):
    global destination_node_ids
    extract_dst_node_ids(node_id)
    for node_id in destination_node_ids:
        if node_id:
            extract_dst_node_ids(node_id)
    if None in destination_node_ids: destination_node_ids.remove(None)
    if '' in destination_node_ids: destination_node_ids.remove('')


def main():

    sys.stdout.flush()


    # list of downstream nodes with the node_id as root taken fron source YAML file
    global nodes
    nodes = []

    # list of IDs of downstream nodes with the node_id as root taken fron source YAML file
    global source_node_ids
    source_node_ids = []

    global destination_node_ids
    destination_node_ids = []

    # dict created from source YAML file. This file will not been changed
    global src_yaml_data
    src_yaml_data = {}

    # initial dict created from destination YAML file
    global dst_yaml_data
    dst_yaml_data = {}

    # new created dict from which new YAML file will be created 
    global new_yaml_data
    new_yaml_data = {}



    [src_file, dst_file, node_id, merge] = ['','','',False]
    try:
        opts, args = getopt.getopt(sys.argv[1:], 's:d:n:mh', ['src_file=', 'dst_file=', 'node_if=', 'merge', 'help'])
    except getopt.GetoptError as err:
        usage_incorrect()
        sys.exit()

    for opt,arg in opts:
        if opt in('-h', '--help'):
            help_info()
            sys.exit()
        elif opt in ('-s', '--src_file'):
            src_file = arg
        elif opt in ('-d', '--dst_file'):
            dst_file = arg
        elif opt in ('-m', '--merge'):
            merge = True
        elif opt in ('-n', '--node_id'):
            node_id = arg
        else:
            usage_incorrect()
            sys.exit()

    if not(src_file and dst_file and node_id):
        usage_incorrect()
        sys.exit()

    input_check(node_id, src_file, dst_file, merge)

   ######### take data from src YAML file ####################

    f_src = open( "%s" % src_file )
    data_src = f_src.read()
    f_src.close()

    try:
        f_dst = open( "%s" % dst_file)
        data_dst = f_dst.read()
        f_dst.close()
    except IOError:
        os.system ('touch %s' % dst_file)
        flag_new_file = 1
        data_dst = ''

    yaml_version = yaml.__version__
    m = re.match('(\d(\.\d)?)', yaml_version)
    yaml_ver = m.group(1)

    if (float(yaml_ver) < 5.1):
        src_yaml_data = yaml.load(data_src)
        dst_yaml_data = yaml.load(data_dst)
 
        
    else:
        src_yaml_data = yaml.load(data_src,Loader=yaml.FullLoader)
        dst_yaml_data = yaml.load(data_dst,Loader=yaml.FullLoader)
        
    if not dst_yaml_data:
        rnode = search_node (src_yaml_data, node_id) 
        initiate_rnode = rnode.copy()
        initiate_rnode['direct_contradictions'] = [{'id':''}]
        initiate_rnode['indirect_contradictions'] = [{'id':''}]
        initiate_rnode['complement'] = [{'id':''}]
        dst_yaml_data = {'statements':[initiate_rnode]}
        print (dst_yaml_data)   
    
    new_yaml_data = dst_yaml_data.copy()

    ######### creation a child YAML file ###################

    get_source_node_ids(node_id)
    print (source_node_ids)
    get_destination_node_ids(node_id)
    print (destination_node_ids)



    with open(dst_file, 'w') as f_dst:
        yaml.dump(new_yaml_data, f_dst, default_flow_style=False, sort_keys=False) 
      
if __name__ == "__main__":
  main() 
