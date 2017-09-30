import networkx as nx
from networkx.drawing.nx_agraph import *

def digraph():
    """
    This function is used to generate a thread-wise view of the entire mailing list by saving the a graph representing the
    messages in a thread as a tree using the References and In-Reply-TO fields from the mail headers. The thread graphs are
    then saved to GEXF, DOT and PNG formats. All authors of a thread are identified and each author is given a unique color.
    All messages sent by this author get the same color.
    """
    discussion_graph = nx.DiGraph()
    color_list = ["#ff0000", "#005555", "#b0b0ff", "#e4e400", "#0000ff", "#ff00ff", "#b000b0", "#870087", "#baba00",
                "#878700", "#545400", "#00ff00", "#8484ff", "#b00000", "#870000", "#550000", "#00b0b0", "#008787",
                "#4949ff", "#550055", "#bababa", "#878787", "#00b000", "#008700", "#005500", "#00ffff"]

    with open("graph_nodes.csv", "r") as node_file:
        for pair in node_file:
            node = pair.split(';', 2)
            discussion_graph.add_node(node[0], time=node[2].strip(), color="#ffffff", style='bold', sender=node[1].strip())
        node_file.close()
    print("Nodes added.")

    # node_list = discussion_graph.nodes()
    with open("graph_edges.csv", "r") as edge_file:
        for pair in edge_file:
            edge = pair.split(';')
            edge[1] = edge[1].strip()
            try:
                discussion_graph.node[edge[0]]['sender']
                discussion_graph.node[edge[1]]['sender']
                discussion_graph.add_edge(*edge)
            except KeyError:
                pass
        edge_file.close()
    print("Edges added.")

    print("No. of Nodes: ", nx.number_of_nodes(discussion_graph))
    print("No. of Edges: ", nx.number_of_edges(discussion_graph))
    print("No. of Weakly Connected Components: ", nx.number_weakly_connected_components(discussion_graph))

    # Uncomment the lines below to save the graph as a GEXF file
    # nx.write_gexf(discussion_graph, "gexf/master_disc_graph.gexf")
    # print("GEXF file generated.")

    # Uncomment the lines below to read the graph from a GEXF file
    # discussion_graph = nx.read_gexf("gexf/master_disc_graph.gexf", node_type=int)
    # print("Graph loaded from GEXF file.")

    for conn_subgraph in nx.weakly_connected_component_subgraphs(discussion_graph):
        sender_color_map = {}
        node_list = [int(x) for x in conn_subgraph.nodes()]
        # Comment the respective lines below to only save in the required formats
        nx.write_gexf(conn_subgraph, 'gexf/' + str(min(node_list))+'.gexf')

        for node_uid in conn_subgraph.nodes():
            try:
                if conn_subgraph.node[node_uid]['sender'] not in sender_color_map:
                    conn_subgraph.node[node_uid]['color'] = color_list[len(sender_color_map) % 26]
                    #print(conn_subgraph.node[node_uid]['color'])
                    sender_color_map[conn_subgraph.node[node_uid]['sender']] = color_list[len(sender_color_map) % 26]
                else:
                    conn_subgraph.node[node_uid]['color'] = sender_color_map[conn_subgraph.node[node_uid]['sender']]
            except:
                for n1,attr in conn_subgraph.nodes(data=True):
                    print(n1, attr)

        g1 = to_agraph(conn_subgraph)
        adj_list1 = conn_subgraph.adjacency_list()
        for neighbour in adj_list1:
            if len(neighbour) > 1:
                g1.add_subgraph([neighbour], rank='same')
        g1.draw('png/' + str(min(node_list))+'.png', prog='dot')
        g1.draw('dot/' + str(min(node_list))+'.dot', prog='dot')

