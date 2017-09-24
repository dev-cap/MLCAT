import csv
from util.read import *


def generate_wh_table_threads(nodelist_filename, edgelist_filename, output_filename, ignore_lat=False, time_limit=None):
    """
    
    Generate the thread width height table, which is a representation of the number of nodes in the graph that have a
    given height and a given number of children in a tabular form. This table provides an aggregate statistical view of
    all the discussion threads and is temporarily stored in a two dimensional array then written into a CSV file.

    :param ignore_lat: If true, then lone author threads are ignored.
    :param time_limit: All messages until this time are considered and all messages after this time are ignored. Time
                       is specified as a string in one of the recognized formats.
    """
    if time_limit is None:
        time_limit = time.strftime("%a, %d %b %Y %H:%M:%S %z")
    msgs_before_time = set()
    time_limit = get_datetime_object(time_limit)
    print("All messages before", time_limit, "are being considered.")

    discussion_graph = nx.DiGraph()
    email_re = re.compile(r'[\w\.-]+@[\w\.-]+')

    # Add nodes into NetworkX graph by reading from CSV file
    if not ignore_lat:
        with open(nodelist_filename, "r") as node_file:
            for pair in node_file:
                node = pair.split(';', 2)
                if get_datetime_object(node[2].strip()) < time_limit:
                    node[0] = int(node[0])
                    msgs_before_time.add(node[0])
                    from_addr = email_re.search(node[1].strip())
                    from_addr = from_addr.group(0) if from_addr is not None else node[1].strip()
                    discussion_graph.add_node(node[0], time=node[2].strip(), color="#ffffff", style='bold', sender=from_addr)
            node_file.close()
        print("Nodes added.")

        # Add edges into NetworkX graph by reading from CSV file
        with open(edgelist_filename, "r") as edge_file:
            for pair in edge_file:
                edge = pair.split(';')
                edge[0] = int(edge[0])
                edge[1] = int(edge[1])
                if edge[0] in msgs_before_time and edge[1] in msgs_before_time:
                    discussion_graph.add_edge(*edge)
            edge_file.close()
        print("Edges added.")

    else:
        lone_author_threads = get_lone_author_threads(False)
        # Add nodes into NetworkX graph only if they are not a part of a thread that has only a single author
        with open(nodelist_filename, "r") as node_file:
            for pair in node_file:
                node = pair.split(';', 2)
                node[0] = int(node[0])
                if get_datetime_object(node[2].strip()) < time_limit and node[0] not in lone_author_threads:
                    msgs_before_time.add(node[0])
                    from_addr = email_re.search(node[1].strip())
                    from_addr = from_addr.group(0) if from_addr is not None else node[1].strip()
                    discussion_graph.add_node(node[0], time=node[2].strip(), color="#ffffff", style='bold', sender=from_addr)
            node_file.close()
        print("Nodes added.")

    # Add edges into NetworkX graph only if they are not a part of a thread that has only a single author
        with open(edgelist_filename, "r") as edge_file:
            for pair in edge_file:
                edge = pair.split(';')
                edge[0] = int(edge[0])
                edge[1] = int(edge[1])
                if edge[0] not in lone_author_threads and edge[1] not in lone_author_threads:
                    if edge[0] in msgs_before_time and edge[1] in msgs_before_time:
                        discussion_graph.add_edge(*edge)
            edge_file.close()
        print("Edges added.")

    # Find out the maximum height of the graph and maximum number of child nodes for any node
    max_width = max(len(i) for i in discussion_graph.adjacency_list())
    max_height = nx.dag_longest_path_length(discussion_graph)
    print("No. of Nodes: ", nx.number_of_nodes(discussion_graph))
    print("No. of Edges: ", nx.number_of_edges(discussion_graph))
    print("No. of Weakly Connected Components: ", nx.number_weakly_connected_components(discussion_graph))
    print("Maximum number of children:", max_width)
    print("Maximum height of the graph:", max_height)

    # The following 2D array stores the number of nodes at given height with a given number of children
    # If A[i][j] = n, then there are n nodes at height i with j children
    wh_table = [[0 for x in range(max_width+1)] for x in range(max_height+1)]
    for conn_subgraph in nx.weakly_connected_component_subgraphs(discussion_graph):
        source_node = min(conn_subgraph.nodes())
        for node in conn_subgraph.nodes():
            node_width = len(conn_subgraph.successors(node))
            try:
                node_height = nx.shortest_path_length(conn_subgraph, source_node, node)
            except:
                node_height = 1
            wh_table[node_height][node_width] += 1
            # print("Node:", node, "Height:",node_height, "Width:",node_width)

    with open(output_filename, 'w') as csvfile:
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
