import networkx as nx
import csv
import re


def generate_wh_table_threads():
    # TODO: Generate the table for a given time interval passed as a parameter.
    discussion_graph = nx.DiGraph()
    email_re = re.compile(r'[\w\.-]+@[\w\.-]+')

    # Add nodes into NetworkX graph by reading CSV files
    with open("graph_nodes.csv", "r") as node_file:
        for pair in node_file:
            node = pair.split(';', 2)
            from_addr = email_re.search(node[1].strip())
            from_addr = from_addr.group(0) if from_addr is not None else node[1].strip()
            discussion_graph.add_node(node[0], time=node[2].strip(), color="#ffffff", style='bold', sender=from_addr)
        node_file.close()
    print("Nodes added.")

    # Add edges into NetworkX graph by reading CSV files
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

    # Find out the maximum height of the graph and maximum number of child nodes for any node
    max_width = max(len(i) for i in discussion_graph.adjacency_list())
    max_height = nx.dag_longest_path_length(discussion_graph)
    print("Maximum number of children:", max_width)
    print("Maximum height of the graph:", max_height)

    # The following 2D array stores the number of nodes at given height with a given number of children
    # If A[i][j] = n, then there are n nodes at height i with j children
    wh_table = [[0 for x in range(max_width+1)] for x in range(max_height+1)]

    for conn_subgraph in nx.weakly_connected_component_subgraphs(discussion_graph):
        node_list = [int(x) for x in conn_subgraph.nodes()]
        source_node = min(node_list)
        # print("Source node:", source_node)
        for node in conn_subgraph.nodes():
            node_width = len(conn_subgraph.successors(node))
            node_height = nx.shortest_path_length(conn_subgraph, str(source_node), node)
            wh_table[node_height][node_width] += 1
            # print("Node:", node, "Height:",node_height, "Width:",node_width)

    with open('wh_table_threads.csv', 'w') as csvfile:
        tablewriter = csv.writer(csvfile)
        tablewriter.writerow(["Height", "Number of children"])
        tablewriter.writerow([" "] + list(range(max_width + 1)) + ["Subtotal"])
        row_height = 0
        total = 0
        for row in wh_table:
            subtotal = 0
            for j in row:
                subtotal += j
            tablewriter.writerow([row_height] + row + [subtotal])
            row_height += 1
            total += subtotal
        tablewriter.writerow(["Total:", total])
        csvfile.close()
        # The line below is a quick test of whether all nodes are accounted for in the table
        assert total == len(discussion_graph.nodes())


generate_wh_table_threads()