import networkx as nx
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as pyplot

discussion_graph = nx.DiGraph()
with open("graph_edges.csv", "r") as edge_file:
    for pair in edge_file:
        edge = pair.split(';')
        edge[1].strip();
        edge[0] = int(edge[0])
        edge[1] = int(edge[1])
        discussion_graph.add_edge(*edge)
    edge_file.close()
print("Edges Added.")

print("No. of Nodes: " + str(len(discussion_graph.nodes())))
print("No. of Edges: " + str(len(discussion_graph.edges())))
print("No. of Weakly Connected Components: " + str(nx.number_weakly_connected_components(discussion_graph)))

# The "weakly_connected_component_subgraphs" function returns a generator for the maximal connected subgraphs of the parameter, here: "discussion_graph".
conn_components = nx.weakly_connected_component_subgraphs(discussion_graph)
conn_subgraph = next(conn_components)

# Here I am plotting only the first two of the components. Ideally we iterate using the generator object "conn_components" to plot for all the subgraphs.
pyplot.axis('off')
nx.draw_networkx(conn_subgraph, arrows=True, with_labels=True, node_size=450, node_color='y', linewidths=0.2,
                 edge_color='0.75', font_size=10)
pyplot.savefig("path-a.png", bbox_inches='tight')

# The clf() function clears all the data in the current plot to make way for other plots.
pyplot.clf()

conn_subgraph = next(conn_components)
pyplot.axis('off')
nx.draw_networkx(conn_subgraph, arrows=True, with_labels=True, node_size=450, node_color='y', linewidths=0.2,
                 edge_color='0.75', font_size=10)
pyplot.savefig("path-b.png", bbox_inches='tight')
