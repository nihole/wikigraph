# -*- coding: utf-8 -*-
import networkx as nx
from networkx.drawing.nx_agraph import write_dot, graphviz_layout
import matplotlib.pyplot as plt


root_label = "Это был яд".decode('utf-8')
label_1 = "Кому он нужен".decode('utf-8')
label_2 = "Карл у Клары украл кораллы".decode('utf-8')
label_3 = "3"
label_4 = "4"
label_5 = "5"

def color (G):
    color_list = []
    gold_nodes = []
    violet_nodes = []
    for node in list(G.nodes):
        path = nx.shortest_path_length(G, source=root_label, target=node, weight=1, method='dijkstra')
        if int(path) % 2:
            gold_nodes.append(node)
            color_list.append("gold")
        else:
            violet_nodes.append(node)
            color_list.append("violet")
    return (color_list, gold_nodes, violet_nodes)

from itertools import islice

def take(n, iterable):
    "Return first n items of the iterable as a list"
    return dict(list(islice(iterable, n)))

G = nx.DiGraph()
G.add_node(root_label)
G.add_node(label_1)
G.add_node(label_2)
G.add_node(label_3)
G.add_node(label_4)
G.add_node(label_5)

G.add_edge(root_label, label_1)
G.add_edge(root_label, label_2)
G.add_edge(label_1, label_3)
G.add_edge(label_2, label_4)
G.add_edge(label_4, label_5)

# color_ = color(G)
(color_list, gold_nodes, violet_nodes) = color(G)
# pos = hierarchy_pos(G,1)
pos =graphviz_layout(G, prog='dot')

print ("GGGGGGGGGGGGGGGGGGGGGGGGGGGG")
print (G)
print ("pospospospospospos")
print (pos)
#nx.draw_networkx_nodes(G, pos=pos,node_color=color_, with_labels=True, node_size=600, node_shape = 's')
#nx.draw_networkx_labels(G, pos=pos,font_size = 6, font_family='sans-serif')
#nx.draw_networkx_edges(G, pos=pos)

bbox_gold = dict(facecolor = "none", edgecolor = "gold", boxstyle = 'round,pad=1')
bbox_violet = dict(facecolor = "none", edgecolor = "violet", boxstyle = 'round,pad=1')

bbox_list = [bbox_gold, bbox_violet, bbox_gold, bbox_violet, bbox_gold ]

# nx.draw(G, pos=pos,node_color=color_list, nodelist = gold_nodes, with_labels=True, node_size=1600, node_shape = 's', font_size = 6, font_family='sans-serif', bbox=bboxx)

#nx.draw(G, pos=pos,node_color='none', with_labels=True, node_size=2000, node_shape = 's', font_size = 6, font_family='sans-serif', bbox = bbox_list)

pos3 = take(3, pos.iteritems())

nx.draw (G, pos3)
nx.draw_networkx_labels(G, pos3, font_size=10, bbox = bbox_gold)

plt.savefig('hierarchy.png')
plt.show()

