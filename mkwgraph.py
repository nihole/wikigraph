import sys
import yaml
import re
import wgraph
import wlib

def single_wcicle(id_dep_lst, dict1, dict2, status_dict):
    for id_dep in id_dep_lst:
        if id_dep in status_dict.keys():
            if status_dict[id_dep] == -1:
                print "Err: dead point is false"
                break
            else:
                status_dict[id_dep] = 1
                status_dict = wlib.node_resolving(id_dep, dict1, dict2, status_dict)

    return status_dict

def wcicles (ref_points_lst, yaml_data):
    status_dict = {}
    (dict1, dict2) = wlib.recurs_dict(yaml_data)
    dead_ends_lst = wlib.deadend(yaml_data, status_dict)
    i = 0
    while len(dead_ends_lst) + len(ref_points_lst):
        print dead_ends_lst
        dd = list(dict.fromkeys(dead_ends_lst + ref_points_lst))
        status_dict = single_wcicle(dd, dict1, dict2, status_dict)
        file_name = 'desdemona_' + str(i) 
        wgraph.wgraph(yaml_data, status_dict, file_name)
        ref_points_lst = []
        i = i + 1
        if i > 10:
            print "Err: Infinitive cicle"
            break
        

if __name__ == "__main__":

    import sys
    import yaml
    import re
    import wgraph

    ref_points_list = ['--14--']

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
    
    wcicles(ref_points_list, yaml_data)
