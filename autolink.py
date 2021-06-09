###################################################################
#                                                                 #
#          Automatically creates links in YAML file               #
#                                                                 #
##################################################################

import sys
import yaml
import re


######### get file's names from the command line ####################
if (len(sys.argv)==3):
    yaml_file = sys.argv[1]
    new_yaml_file = sys.argv[2]
else:
    print ("   ######################################################\n")
    print ("   Syntax is:\n")
    print ("   python autolink.py old_file.yml new_file.yml  \n")
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

for record in yaml_data:
    id = record['id']
    m = re.find('--(\d+)--', id)
    p = re.find('++(\d+)++', id)
    if m:
        number = m.group(0)
        link = https://github.com/nihole/wg_navalny/wiki/nw_number
     if p:
        number = m.group(0)
        link = https://github.com/nihole/wg_navalny/wiki/pw_number
    record['wiki_link'] = link

with open(new_yaml_file, 'w') as outfile:
    yaml.dump(yaml_data, outfile, default_flow_style=False)

