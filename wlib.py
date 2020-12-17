# hello.py - http://www.graphviz.org/content/hello
# -*- coding: utf-8 -*-

### The library for wave graf relolving



def check_direct_contr(record):
### Check if there are direct contradictioans in the record related to the node (statemenet)
### Returns 1 if there is direct contradictioans to this statement
    if len(record['direct_contradictions'])==1:
        if not record['direct_contradictions'][0]['id']:
            flag_dc = 0
        else:
            flag_dc = 1
    elif len(record['direct_contradictions'])==0:
        flag_dc = 0
    else:
        flag_dc = 1
    return flag_dc

def check_indirect_contr(record):
### Check if there are indirect contradoctioans in the record related to the node (statemenet)
### Returns 1 if there are
    if len(record['indirect_contradictions'])==1:
        if not record['indirect_contradictions'][0]['id']:
            flag_ic = 0
        else:
            flag_ic = 1
    elif len(record['indirect_contradictions'])==0:
        flag_ic = 0
    else:
        flag_ic = 1
    return flag_ic

def check_complement(record):
### Check if there are complement statements in the record related to the node (statemenet)
### Returns 1 if there are
    if len(record['complement'])==1:
        if not record['complement'][0]['id']:
            flag_c = 0
        else:
            flag_c = 1
    elif len(record['complement'])==0:
        flag_c = 0
    else:
        flag_c = 1
    return flag_c

def deadend(yml_data, status_dict):
### Returns a list of dead-endsdirect contradictioansof graf repesented ib yml_data
### Dead-end is a statement without any type of contradictions, direct, indirect or complement
    deadends = []
    
    for i in range(len(yml_data['statements'])):
        flag = 0
        record = yml_data['statements'][i]
        (rdict, reverse_rdict) = recurs_dict (yml_data)
        if check_complement(record):
            [cmpl] = rdict[record['id']]['complement']
            if (( cmpl not in status_dict.keys()) or (not status_dict[cmpl]==-1) or (not status_dict[cmpl]==-0)):
                flag = 1
        elif check_direct_contr(record):
            direct_contr_list = rdict[record['id']]['direct']
            if len(direct_contr_list):
                for dcid in direct_contr_list:
                    if ((dcid not in status_dict.keys()) or (not status_dict[dcid]==-1) or (not status_dict[dcid]==-0)):
                        flag = 1
                        break
        elif check_indirect_contr(record):
            indirect_contr_list = rdict[record['id']]['indirect']
            if len(indirect_contr_list):
                for indcid in indirect_contr_list:
                    if ((indcid not in status_dict.keys()) or (not status_dict[indcid]==-1) or (not status_dict[indcid]==-0)):
                        flag = 1
                        break

        if not flag:
            deadends.append(record['id'])
    return (deadends)

def find_seq_id(yml_data, id_):
### Return seq number of list element (yml_data) with id = id_
    seq = -1
    for i in range(len(yml_data["statements"])):
        m = re.match(id_, yml_data["statements"][i]["id"])
        if m:
            seq = i
            break
    return seq

def recurs_dict (yml_data):
### Returns recursive dictionaries: direct (downstream) and revers (upstream)
### rdict - direct recursion from root towards ends, and reverse_rdict - recursion towards root 
### the structure of them is {node_id:{'direct':[node_ids],'indirect':[node_ids],'complement':[node_ids]}, ...}
    rdict = {}
    reverse_rdict = {}
    ### Initiation
    for record_ in yml_data['statements']:
        node = record_['id']
        if node not in rdict.keys():
            rdict[node] = {}
            rdict[node]['direct'] = []
            rdict[node]['indirect'] = []
            rdict[node]['complement'] = []
        if node not in reverse_rdict.keys():
            reverse_rdict[node] = {}
            reverse_rdict[node]['direct'] = []
            reverse_rdict[node]['indirect'] = []
            reverse_rdict[node]['complement'] = []
    for record in yml_data['statements']:
        dnode = record['id']
        if check_direct_contr(record):
            for element in record['direct_contradictions']:
                rnode = element['id']
                rdict[dnode]['direct'].append(rnode)
                reverse_rdict[rnode]['direct'].append(dnode)
        if check_indirect_contr(record):
            for element in record['indirect_contradictions']:
                rnode = element['id']
                rdict[dnode]['indirect'].append(rnode)
                reverse_rdict[rnode]['indirect'].append(dnode)
        if check_complement(record):
            if len(record['complement']) > 1:
                print "Only a single complement contradiction is possible!"
            else: 
                [element] = record['complement']
                rnode = element['id']
                rdict[dnode]['complement'] = [rnode]
                rdict[rnode]['complement'] = [dnode]
                reverse_rdict[dnode]['complement'] = [rnode]
                reverse_rdict[rnode]['complement'] = [dnode]
    return (rdict, reverse_rdict) 

def path_check (id_, rdict,  reverse_rdict, status_dict):
### If we know the status of node with id = id_ (1 - true, 0 - false, -1 - deleted)
### then next step downstream nodes with only one reverse path to root via this
### node (id = id_) should be marked as deleted (-1)
    
    ### initiation of lists with such nodes for direct, inderect, complement edges:
    dnode_list = []
    inode_list = []
    cnode_list = []
    if id_ in rdict.keys():
        for dnode_ in list(set(rdict[id_]['direct'] + rdict[id_]['indirect'] + rdict[id_]['complement'])):
            all_reverse_node = list(set(reverse_rdict[dnode_]['direct'] + reverse_rdict[dnode_]['indirect'] + reverse_rdict[dnode_]['complement']))
            flag = 0
            for reverse_node_ in all_reverse_node:
                if (reverse_node_ in status_dict.keys()) and not ( status_dict[reverse_node_] == -1):
                    flag = 1
                    break

            if not flag:
                status_dict[dnode_]=-1
                dnode_list.append(dnode_)
    ### return the list of removed downstream nodes and new status_dict

        return (dnode_list + inode_list + cnode_list, status_dict)
    else:
        return ([], status_dict)

def recurse_path_check (id_, rdict,  reverse_rdict, status_dict):
    import copy
### using step by step recursion (path_check) marks as deleted all downstram nodes
### having a single path to root via the node with id = id_
    node_list = [id_]
    i = 0 # for infinitive cicle avoiding
    while len(node_list) > 0:
        print (node_list)
        node_lst = []
        ### this will be commulative node list
        for node in node_list:
            node_l = []
            (node_l, status_dict) = path_check(node, rdict,  reverse_rdict, status_dict)
            node_lst = node_lst + node_l
            node_lst = list(dict.fromkeys(node_lst))
        node_list = copy.copy(node_lst)
        ### to avoid infinitive cicles
        i=i+1
        if i>100:
            print ('Infinitive cicle!!')
            break
    return status_dict

def node_resolving (id_, rdict, reverse_rdict, status_dict):
## return dictionary ststus_dict. Keys - ids of nodes (statements), values: 1,-1,0, 777 
### 1 means true, 0 - false, -1 - lost path to the root. 777 is used to label a conflict (true/false) 
    
    ### we always start with the element we believe the truth
    status_dict[id_] = 1
    ### mark as deleted (-1) all downstreem nodes (for all types of edge) 
    ### if they have path to root only via this node
    status_dict = recurse_path_check(id_, rdict,  reverse_rdict, status_dict)

    reverse_direct_and_complement = reverse_rdict[id_]['direct']+reverse_rdict[id_]['complement']
    for dnode in reverse_direct_and_complement:
        ### if this statement is truth then statements for which this one is direct controdition are false
        ### first check wheher these direct upstream statements already marked as 1,0,-1
        if dnode in status_dict.keys(): 
            if status_dict[dnode] == -1:
                continue
            elif status_dict[dnode] == 1:
                ### this means conflict
                return {dnode:777}
        else:
            status_dict[dnode] = 0
    return status_dict
    
#def deadends_resolving():
 #   def graph_resolving():


if __name__ == "__main__":

    import sys
    import yaml
    import re
    import wgraph

    ## For test purpose we consider node with id '--14--' as truth (dead-end node)

    id_dep = '--14--'

    ######### get file's names from the command line ####################
    if (len(sys.argv)==2):
        yaml_file = sys.argv[1]
    else:
        print ("   ######################################################\n")
        print ("   Syntax is:\n")
        print ("   python3 ../../wlib.py desdemona.yml \n")
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

    (dict1, dict2) = recurs_dict(yaml_data)
    dd = deadend(yaml_data, {})
    status_dict_ = node_resolving(id_dep, dict1, dict2, {})
    print status_dict_

    wgraph.wgraph(yaml_data, status_dict_, 'desdemona')
