import networkx as nx
import pygraphviz as pgv

discussion_graph = nx.DiGraph()
with open("graph_edges.csv", "r") as edge_file:
    for pair in edge_file:
        edge = pair.split(';')
        edge[1] = int(edge[1])
        edge[0] = int(edge[0])
        discussion_graph.add_edge(*edge)
    edge_file.close()
print("Edges added.")

print("No. of Nodes: " + str(nx.number_of_nodes(discussion_graph)))
print("No. of Edges: " + str(nx.number_of_edges(discussion_graph)))
print("No. of Weakly Connected Components: " + str(nx.number_weakly_connected_components(discussion_graph)))

# Uncomment the lines below to save the graph as a GEXF file
# nx.write_gexf(discussion_graph, "gexf/master_disc_graph.gexf")
# print("GEXF file generated.")

# Uncomment the lines below to read the graph from a GEXF file
# discussion_graph = nx.read_gexf("gexf/master_disc_graph.gexf", node_type=int)
# print("Graph loaded from GEXF file.")

# The "weakly_connected_component_subgraphs" function returns a generator for the maximal connected subgraphs of the parameter.
# conn_components = nx.weakly_connected_component_subgraphs(discussion_graph)

for conn_subgraph in nx.weakly_connected_component_subgraphs(discussion_graph):
    # conn_subgraph = next(conn_components)
    g1 = nx.to_agraph(conn_subgraph)
    adj_list1 = conn_subgraph.adjacency_list()
    for neighbour in adj_list1:
        if len(neighbour) > 1:
            g1.add_subgraph([neighbour], rank='same')
    g1.draw('png/' + str(min(conn_subgraph.nodes()))+'.png', prog='dot')
    g1.draw('dot/' + str(min(conn_subgraph.nodes()))+'.dot', prog='dot')

