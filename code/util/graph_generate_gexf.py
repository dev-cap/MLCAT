import networkx as nx

discussion_graph = nx.DiGraph()

with open("graph_nodes.csv", "r") as node_file:
    for pair in node_file:
        node = pair.split(';', 1)
        discussion_graph.add_node(node[0], time=node[1].strip(), color="#000000", style='bold')
    node_file.close()
print("Nodes added.")

with open("graph_edges.csv", "r") as edge_file:
    for pair in edge_file:
        edge = pair.split(';')
        edge[1] = edge[1].strip()
        discussion_graph.add_edge(*edge)
    edge_file.close()
print("Edges added.")

print("No. of Nodes: " + str(len(discussion_graph.nodes())))
print("No. of Edges: " + str(len(discussion_graph.edges())))
print("No. of Weakly Connected Components: " + str(nx.number_weakly_connected_components(discussion_graph)))

# Uncomment the lines below to save the entire graph as a GEXF file
# nx.write_gexf(discussion_graph, "gexf/master_disc_graph.gexf")
# print("Master GEXF file written to disk.")

for conn_subgraph in nx.weakly_connected_component_subgraphs(discussion_graph):

    nx.write_gexf(conn_subgraph, 'gexf/' + str(min(conn_subgraph.nodes()))+'.gexf')

print("GEXF files for all threads written to disk.")