# hello.py - http://www.graphviz.org/content/hello
# -*- coding: utf-8 -*-



def check_direct_contr(record):
### Check if there are a direct contradoctioans in the record related to node (statemenet)
### Returns 1 if there are 
    if len(record['direct_contradictions'])==1:
        if not record['direct_contradictions'][0]['id']:
            flag_dc = 1
        else:
            flag_dc = 0
    elif len(record['direct_contradictions'])==0:
        flag_dc = 1
    else:
        flag_dc = 0
    return flag_dc

def check_indirect_contr(record):
### Check if there are an indirect contradoctioans in the record related to node (statemenet)
### Returns 1 if there are
    if len(record['indirect_contradictions'])==1:
        if not record['indirect_contradictions'][0]['id']:
            flag_ic = 1
        else:
            flag_ic = 0
    elif len(record['indirect_contradictions'])==0:
        flag_ic = 1
    else:
        flag_ic = 0
    return flag_ic

def check_complement(record):
### Check if there are an indirect contradoctioans in the record related to node (statemenet)
### Returns 1 if there are
    if len(record['complement'])==1:
        if not record['complement'][0]['id']:
            flag_c = 1
        else:
            flag_c = 0
    elif len(record['complement'])==0:
        flag_c = 1
    else:
        flag_c = 0
    return flag_c

def deadend(yml_data):
### Returns a list of dead-ends
### Dead-end is a statement without contradictions, direct or indirect
    deadends = []
    for i in range(len(yml_data['statements'])):
        record = yml_data['statements'][i]
                
        if (check_direct_contr(record) and check_indirect_contr(record)):
            deadends.append((i, record['id']))
    return (deadends)

def find_seq_id(yml_data, id_):
    seq = -1
    for i in range(len(yml_data["statements"])):
        m = re.match(id_, yml_data["statements"][i]["id"])
        if m:
            seq = i
            break
    return seq

def recurs_dict (yml_data):
### Returns recursive dictionaries. 
### rdict - recursion from root towards ends, and reverse_rdict - recursion towards root 
    rdict = {}
    reverse_rdict = {}
    for record in yml_data['statements']:
        dnode = record['id']
        if record['id'] not in rdict.keys():
            rdict[dnode] = {}
            rdict[dnode]['direct'] = []
            rdict[dnode]['indirect'] = []
            rdict[dnode]['complement'] = []
        if not check_direct_contr(record):
            for element in record['direct_contradictions']:
                rdict[dnode]['direct'].append(element['id'])
                rnode = element['id']
                if element['id'] not in reverse_rdict.keys():
                    reverse_rdict[rnode] = {}
                    reverse_rdict[rnode]['direct'] = []
                    reverse_rdict[rnode]['indirect'] = []
                    reverse_rdict[rnode]['complement'] = []
                reverse_rdict[rnode]['direct'].append(dnode)
        if not check_indirect_contr(record):
            for element in record['indirect_contradictions']:
                rdict[dnode]['indirect'].append(element['id'])
                rnode = element['id']
                if element['id'] not in reverse_rdict.keys():
                    reverse_rdict[rnode] = {}
                    reverse_rdict[rnode]['direct'] = []
                    reverse_rdict[rnode]['indirect'] = []
                    reverse_rdict[rnode]['complement'] = []
                reverse_rdict[rnode]['indirect'].append(dnode)
        if not check_complement(record):
            for element in record['complement']:
                rdict[dnode]['complement'].append(element['id'])
                rnode = element['id']
                if element['id'] not in reverse_rdict.keys():
                    reverse_rdict[rnode] = {}
                    reverse_rdict[rnode]['direct'] = []
                    reverse_rdict[rnode]['indirect'] = []
                    reverse_rdict[rnode]['complement'] = []
                reverse_rdict[rnode]['complement'].append(dnode)
    return (rdict, reverse_rdict) 


import sys
import yaml
import re

    ######### get file's names from the command line ####################
if (len(sys.argv)==2):
    yaml_file = sys.argv[1]
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

# print deadend(yaml_data)
(dict1, dict2) = recurs_dict(yaml_data)
print dict1
print "\n\n\n"
print dict2
