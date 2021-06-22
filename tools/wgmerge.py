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
def merge_data (node_id)			- merges
'''

import sys
import re
import yaml
import getopt
import pathlib
import os
sys.path.insert(1,"%s/.." % pathlib.Path(__file__).parent.absolute())
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

def merge_data (node_id):
    global source_node_ids
    global destination_node_ids 
    global src_yaml_data
    global destination_yaml_data
    global new_yaml_data
    for id_source in source_node_ids:
        if id_source in destination_node_ids:
            node_new = search_node (new_yaml_data, node_id)
            node_source = search_node (src_yaml_data, id_source)
            node_destination = search_node (dst_yaml_data, id_source)
            direct_src_ids = []
            indirect_src_ids = []
            complement_src_ids = []
            direct_dst_ids = []
            indirect_dst_ids = []
            complement_dst_ids = []
            diff_direct = []
            diff_indirect = []
            diff_complement = []

            for el_src in node_source['direct_contradictions']:
                    if el_src:
                        direct_src_ids.append(el_src['id'])
            for el_src in node_source['indirect_contradictions']:
                    if el_src:
                        indirect_src_ids.append(el_src['id'])
            for el_src in node_source['complement']:
                    if el_src:
                        complement_src_ids.append(el_src['id']) 
            for el_dst in node_destination['direct_contradictions']:
                    if el_dst:
                        direct_dst_ids.append(el_dst['id'])
            for el_dst in node_destination['indirect_contradictions']:
                    if el_dst:
                        indirect_dst_ids.append(el_dst['id'])
            for el_dst in node_destination['complement']:
                    if el_dst:
                        complement_dst_ids.append(el_dst['id']) 
            diff_direct = list(set(direct_src_ids) -set(direct_dst_ids))
            if None in diff_direct: diff_direct.remove(None)
            if '' in diff_direct: diff_direct.remove('')
            diff_indirect = list(set(indirect_src_ids) - set(indirect_dst_ids))
            if None in diff_indirect: diff_indirect.remove(None)
            if '' in diff_indirect: diff_indirect.remove('')
            diff_complement = list(set(complement_src_ids) - set(complement_dst_ids))
            if None in diff_complement: diff_complement.remove(None)
            if '' in diff_complement: diff_complemnet.remove('')
          
            if (len(diff_direct) > 0)  and (len(direct_dst_ids) == 1) and (node_new['direct_contradictions'][0]['id'] == None):
                node_new['direct_contradictions'].remove({'id':None})
            for diff_el in diff_direct:
                node_new['direct_contradictions'].append({'id':diff_el})
            if (len(diff_indirect) > 0)  and (len(indirect_dst_ids) == 1) and (node_new['indirect_contradictions'][0]['id'] == None):
                node_new['indirect_contradictions'].remove({'id':None})
            for diff_el in diff_indirect:
                node_new['indirect_contradictions'].append({'id':diff_el})
            if (len(diff_complement) > 0)  and (len(complement_dst_ids) == 1) and (node_new['complement'][0]['id'] == None) :
                node_new['complement'].remove({'id':None})  
            for diff_el in diff_complement:
                node_new['complement'].append({'id':diff_el}) 
        else:
            node_source = search_node (src_yaml_data, id_source)
            new_yaml_data['statements'].append(node_source)   

def rewrite_data (node_id):
    global source_node_ids
    global destination_node_ids 
    global src_yaml_data
    global destination_yaml_data
    global new_yaml_data
    global reverse_dst_yaml_data

    diff_up_dst_ids = []
    summ_node_ids = list(set(source_node_ids + destination_node_ids))
    summ_node_ids.append(node_id)
    for id_summ in summ_node_ids:
        if (id_summ in source_node_ids) and not (id_summ in destination_node_ids):
            node_source = search_node (src_yaml_data, id_summ)
            new_yaml_data['statements'].append(node_source)
        elif (id_summ in source_node_ids) and (id_summ in destination_node_ids):
            if new_yaml_data['statements'][0]['id']==node_id:
                node_source = search_node (src_yaml_data, id_summ)
                new_yaml_data['statements'][0] = node_source
            else: 
                node_destination = search_node (dst_yaml_data, id_summ)
                node_source = search_node (src_yaml_data, id_summ)
                new_yaml_data['statements'].remove(node_destination)
                new_yaml_data['statements'].append(node_source)
        else:
            upsream_ids = reverse_dst_yaml_data[0][id_summ]['direct'] + reverse_dst_yaml_data[0][id_summ]['indirect'] + reverse_dst_yaml_data[0][id_summ]['complement']
            diff_up_dst_ids = list(set(upsream_ids) - set(destination_node_ids))
            if None in diff_up_dst_ids: diff_up_dst_ids.remove(None)
            if '' in diff_up_dst_ids: diff_up_dst_ids.remove('')
            if len(diff_up_dst_ids) > 0:
                node_new = search_node (new_yaml_data, id_summ)
                if not (node_new['direct_contradictions'][0]['id'] == None):
                    for el_ in node_new['direct_contradictions']:
                        if not el_['id'] in source_node_ids:
                            node_new['direct_contradictions'].remove(el_)
                    if len(node_new['direct_contradictions']) == 0:
                        node_new['direct_contradictions'].append({'id':None})
                else:
                    new_yaml_data['statements'].remove(node_source)
                if not (node_new['indirect_contradictions'][0]['id'] == None):
                    for el_ in node_new['indirect_contradictions']:
                        if not el_['id'] in source_node_ids:
                            node_new['indirect_contradictions'].remove(el_)
                    if len(node_new['indirect_contradictions']) == 0:
                        node_new['indirect_contradictions'].append({'id':None})
                else:
                    new_yaml_data['statements'].remove(node_source)
                if not (node_new['complement'][0]['id'] == None):
                    for el_ in node_new['complement']:
                        if not el_['id'] in source_node_ids:
                            node_new['complement'].remove(el_)
                    if len(node_new['complement']) == 0:
                        node_new['complement'].append({'id':None})
                else:
                    new_yaml_data['statements'].remove(node_source)
            else:
                node_new = search_node (new_yaml_data, id_summ)
                new_yaml_data['statements'].remove(node_new)    
    

      

### Creates a full list of node ids in waves starting with node_id taken from source file

def get_source_node_ids (node_id):
    global source_node_ids
    extract_src_node_ids(node_id)
    for id_ in source_node_ids:
        if id_:
            extract_src_node_ids(id_)
    if None in source_node_ids: source_node_ids.remove(None)
    if '' in source_node_ids: source_node_ids.remove('')
    source_node_ids.append(node_id)

### Creates a full list of node ids in waves starting with node_id taken from destination file

def get_destination_node_ids (node_id):
    global destination_node_ids
    extract_dst_node_ids(node_id)
    for id_ in destination_node_ids:
        if id_:
            extract_dst_node_ids(id_)
    if None in destination_node_ids: destination_node_ids.remove(None)
    if '' in destination_node_ids: destination_node_ids.remove('')
    destination_node_ids.append( node_id)


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

    global reverse_dst_yaml_data
    reverse_dst_yaml_data =  []



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
        initiate_rnode['direct_contradictions'] = [{'id':None}]
        initiate_rnode['indirect_contradictions'] = [{'id':None}]
        initiate_rnode['complement'] = [{'id':None}]
        dst_yaml_data = {'statements':[initiate_rnode]}
    
    new_yaml_data = dst_yaml_data.copy()

    ######### creation a child YAML file ###################
    get_source_node_ids (node_id)
    get_destination_node_ids (node_id)

    reverse_dst_yaml_data = wlib.recurs_dict(dst_yaml_data)
    
    if merge:
        merge_data(node_id)
    else:
        rewrite_data(node_id)
#    get_source_node_ids(node_id)
#    print (source_node_ids)
#    get_destination_node_ids(node_id)
#    print (destination_node_ids)



    with open(dst_file, 'w') as f_dst:
        yaml.dump(new_yaml_data, f_dst, default_flow_style=False, sort_keys=False, allow_unicode=True)
      
if __name__ == "__main__":
  main() 
