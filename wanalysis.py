# hello.py - http://www.graphviz.org/content/hello
# -*- coding: utf-8 -*-

def deadend(yml_data):
    deadends = []
    for i in range(len(yml_data['statements'])):
        record = yml_data['statements'][i]
        if len(record['direct_contradictions'])==1:
            if not record['direct_contradictions'][0]['id']:
                flag_dc = 1
            else:
                flag_dc = 0
        elif len(record['direct_contradictions'])==0:
            flag_dc == 1
        else:
            flag_dc = 0

        if len(record['indirect_contradictions'])==1:
            if record['indirect_contradictions'][0]['id'] == '':
                flag_ic = 1
        elif len(record['indirect_contradictions'])==0:
            flag_ic == 1
        else:
            flag_ic = 0

                
        if flag_dc:
            deadends.append((i, record['id']))
    return (deadends)
        

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

print deadend(yaml_data)
