import networkx as nx
from networkx.drawing.nx_agraph import write_dot, graphviz_layout
import matplotlib.pyplot as plt

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


# write dot file to use with graphviz
# run "dot -Tpng test.dot >test.png"
write_dot(G,'test.dot')

# same layout using matplotlib with no labels
plt.title('draw_networkx')
pos =graphviz_layout(G, prog='dot')
nx.draw(G, pos, with_labels=True, arrows=True)
# plt.savefig('nx_test.png')
plt.show()

