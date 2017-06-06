import csv
from util.read_utils import *


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

    add_elements_to_graph(ignore_lat,nodelist_filename,time_limit,msgs_before_time,email_re,edgelist_filename,discussion_graph)

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