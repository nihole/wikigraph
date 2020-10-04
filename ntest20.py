import networkx as nx
from networkx.drawing.nx_agraph import write_dot, graphviz_layout
import matplotlib.pyplot as plt


def color(G):
    color_list = []
    for node in list(G.nodes):
        path = nx.shortest_path_length(G, source="ROOT", target=node, weight=1, method='dijkstra')
        if int(path) % 2:
            color_list.append("gold")
        else:
            color_list.append("violet")
    return color_list


G = nx.DiGraph()
G.add_node("ROOT")
G.add_node("TEST 1")
G.add_node("TEST 2")
G.add_node("TEST 3")
G.add_node("TEST 4")
G.add_node("TEST 5")

G.add_edge("ROOT", "TEST 1")
G.add_edge("ROOT", "TEST 2")
G.add_edge("TEST 1", "TEST 3")
G.add_edge("TEST 2", "TEST 4")
G.add_edge("TEST 4", "TEST 5")

color_ = color(G)
# pos = hierarchy_pos(G,1)
pos =graphviz_layout(G, prog='dot')
#nx.draw_networkx_nodes(G, pos=pos,node_color=color_, with_labels=True, node_size=600, node_shape = 's')
#nx.draw_networkx_labels(G, pos=pos,font_size = 6, font_family='sans-serif')
#nx.draw_networkx_edges(G, pos=pos)
nx.draw(G, pos=pos,node_color=color_, with_labels=True, node_size=1600, node_shape = 's', font_size = 6, font_family='sans-serif', bbox = dict(facecolor = "none", edgecolor = "black", boxstyle = 'round,pad=1'))
plt.savefig('hierarchy.png')
plt.show()

