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
import getopt

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


def search_node (node_id):
    global src_yaml_data
    flag = 0
    for node in src_yaml_data['statements']:
        if node['id'] == node_id:
            flag = 1
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


def main():

    sys.stdout.flush()


    # list of downstream nodes with the node_id as root taken fron source YAML file
    global nodes

    # list of IDs of downstream nodes with the node_id as root taken fron source YAML file
    global new_node_ids

    # dict created from source YAML file. This file will not been changed
    global src_yaml_data

    # initial dict created from destination YAML file
    global dst_yaml_data

    # new created dict from which new YAML file will be created 
    global new_yaml_data


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

    f_dst = open( "%s" % dst_file, 'w+')
    data_dst = f_dst.read()
    f_dst.close()

    yaml_version = yaml.__version__
    m = re.match('(\d(\.\d)?)', yaml_version)
    yaml_ver = m.group(1)

    if (float(yaml_ver) < 5.1):
        src_yaml_data = yaml.load(data_src)
        dst_yaml_data = yaml.load(data_dst)
        
    else:
        src_yaml_data = yaml.load(data_src,Loader=yaml.FullLoader)
        dst_yaml_data = yaml.load(data_dst,Loader=yaml.FullLoader)

    ######### creation a child YAML file ###################

    nodes = []
    new_node_ids = []
    new_yaml_data = {'statements':nodes}

    add_node(node_id)
    for node_id in new_node_ids:
        if node_id:
            add_node(node_id)
    



    with open(dst_file, 'w') as f_dst:
        yaml.dump(new_yaml_data, f_dst, default_flow_style=False, sort_keys=False) 
      
if __name__ == "__main__":
  main() 
