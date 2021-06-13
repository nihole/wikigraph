# hello.py - http://www.graphviz.org/content/hello
# -*- coding: utf-8 -*-

###################################################################
#                                                                 #
#    Extracts a sub-wikigraph with a particular node as root      #
#                                                                 #
##################################################################

import sys
import re


######### get file's names from the command line ####################
if (len(sys.argv)==4):
    yaml_file = sys.argv[1]
    new_yaml_file = sys.argv[2]
    node_id = sys.argv[3]
else:
    print ("   ######################################################\n")
    print ("   Syntax is:\n")
    print ("   python extract.py parent_wikigraph_yaml.yml sub_wikigraph.yml node_id \n")
    print ("   ######################################################\n")
    quit()


   ######### take data from YAML file ####################

config = ''
with open(yaml_file, 'r') as inputfile:
    m = p = l = flag_m = flag_p = 0
    for line in inputfile:
        m = re.search('^- id:.+--\d+--', line)
        p = re.search('^- id:.+\+\+\d+\+\+', line)
        l = re.search('wiki_link', line)
        if m:
            flag_m = 1
            m1 = re.search('\d+', line)
            number = m1.group(0)
            config = config + line
        elif p:
            flag_p = 1
            p1 = re.search('\d+', line)
            number = p1.group(0)
            config = config + line
        elif l:
            if flag_m:
                new_line = '  wiki_link: ' + 'https://github.com/nihole/wg_navalny/wiki/nw_' + number + '\n'
                flag_m = 0
                config = config + new_line
            if flag_p:
                new_line = '  wiki_link: ' + 'https://github.com/nihole/wg_navalny/wiki/pw_' + number + '\n'
                flag_p = 0
                config = config + new_line
        else:
            config = config + line


with open(new_yaml_file, 'w') as outfile:
    outfile.write(config)

