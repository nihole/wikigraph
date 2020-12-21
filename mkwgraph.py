import sys
import yaml
import re
import wgraph
import wlib

def single_wcicle(id_truth_lst, root_id, dict1, dict2, status_dict, paths_dict):
    # id_truth_lst - dead ends (without any contradicions) and reference points ( taken for truth )
    # dict1 - recurse dictionary: 
    # - dict1['statement_id']['direct'] = [list of ids of  direct contradictions]
    # - dict1['statement_id']['indirect'] = [list of ids of indirect contradictions]
    # - dict1['statement_id']['complementary'] = [list of ids of complementary contradictions]
    # dict2 - reverse dictionary - the same as dict1 but in opposit direction
    
    for id_dep in id_truth_lst:
        print (id_dep)
        print (status_dict)
        if id_dep in status_dict.keys():
            print (id_dep)
            print (status_dict[id_dep])
            if status_dict[id_dep] == 0:
                # The dead center must be true, and if this is a false, this means we have some inconsistency in the logic.
                quit ("Err: dead point %s is false" % id_dep)
        status_dict[id_dep] = 1
        status_dict = wlib.node_resolving(id_dep, root_id, dict1, dict2, status_dict, paths_dict)

    return status_dict

def wcicles (ref_points_lst, yaml_data):
    # Initiating and checkinf YAML configuration
    status_dict = {}
    (root_id, rdict, reverse_rdict, phase,  paths_dict) = wlib.check_structure (yaml_data)
    dead_ends_lst = wlib.deadend(yaml_data, status_dict)

#    dead_ends_lst = []
    i = 0
    while (len(dead_ends_lst) + len(ref_points_lst) > 0):
        dd = list(set(dead_ends_lst + ref_points_lst))
        print (dd)
        status_dict = single_wcicle(dd, root_id, rdict, reverse_rdict, status_dict, paths_dict)

        file_name = 'desdemona_' + str(i) 
        wgraph.wgraph(yaml_data, status_dict, phase, file_name)
        dead_ends_lst = wlib.deadend(yaml_data, status_dict)
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

    ref_points_list = ['--14--', '--13--']

    ######### get file's names from the command line ####################
    if (len(sys.argv)==2):
        yaml_file = sys.argv[1]
    else:
        print ("   ######################################################\n")
        print ("   Syntax is:\n")
        print ("   python mkwgraph.py wikigraphs/desdemona/desdemona.yml \n")
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
