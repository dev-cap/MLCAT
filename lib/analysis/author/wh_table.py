import csv
from util.read import *


def generate_wh_table_authors(nodelist_filename, edgelist_filename, output_filename, ignore_lat=False, time_limit=None):
    """
    This module is used to generate the author version of the width height table. The width height table for the
    authors is a representation of the number of total and new authors in a thread aggregated at a given generation.
    The table, which itself is temporarily stored in a two dimensional array, is then written into a CSV file. These
    tables are can be used to decipher the basic conversation structure.

    :param nodelist_filename: The csv file containing the nodes.
    :param edgelist_filename: The csv file containing the edges.
    :param output_filename: Stores the width-height table values.
    :param ignore_lat: If true, then lone author threads are ignored.
    :param time_limit: All messages until this time are considered and all messages after this time are ignored. Time is specified as a string in one of the recognized formats.
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
                    try:
                        discussion_graph.node[edge[0]]['sender']
                        discussion_graph.node[edge[1]]['sender']
                        discussion_graph.add_edge(*edge)
                    except KeyError:
                        pass
            edge_file.close()
        print("Edges added.")

    else:
        lone_author_threads = get_lone_author_threads()
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
    max_height = nx.dag_longest_path_length(discussion_graph)

    # The following 2D array stores the number of nodes at given height with a given number of children
    # If A[i][j] = n, then there are n nodes at height i with j children
    new_wh_table = [[0 for x in range(nx.number_of_nodes(discussion_graph)//2)] for x in range(max_height+1)]
    wh_table = [[0 for x in range(nx.number_of_nodes(discussion_graph)//2)] for x in range(max_height+1)]
    max_width = 0

    for conn_subgraph in nx.weakly_connected_component_subgraphs(discussion_graph):
        # The following lists of sets store the authors / new authors at each level in the thread.
        authors_at_height = [set() for x in range(max_height+1)]
        new_authors_at_height = [set() for x in range(max_height+1)]
        thread_authors = set()
        source_node = min(conn_subgraph.nodes())
        # print("Source node:", source_node)
        for node, attributes in sorted(conn_subgraph.nodes_iter(data=True)):
            node_author = attributes['sender']
            try:
                node_height = nx.shortest_path_length(conn_subgraph, source_node, node)
            except:
                node_height = 1
            authors_at_height[node_height].add(node_author)
            if node_author not in thread_authors:
                new_authors_at_height[node_height].add(node_author)
            thread_authors.add(node_author)

        for height in range(max_height+1):
            wh_table[height][len(authors_at_height[height])] += 1
        for height in range(max_height+1):
            new_wh_table[height][len(new_authors_at_height[height])] += 1
        # print("Node:", node, "Height:",node_height, "Width:",node_width)
        thread_max_width = max([len(i) for i in authors_at_height])
        max_width = thread_max_width if max_width < thread_max_width else max_width

    irow = 0
    combined_table = [[0 for x in range(2 * max_width)] for x in range(max_height+1)]
    for (row1, row2) in zip(wh_table, new_wh_table):
        icol = 0
        row1 = row1[1:max_width+1]
        row2 = row2[1:max_width+1]
        for i in range(max_width):
            combined_table[irow][icol] = row1[i]
            combined_table[irow][icol+1] = row2[i]
            icol += 2
        irow += 1

    with open(output_filename, 'w') as csvfile:
        tablewriter = csv.writer(csvfile)
        tablewriter.writerow(["Height(h)", "Number of authors(i)"])
        tablewriter.writerow([" "] + "  ".join([str(x) for x in range(1, max_width + 1)]).split(" ") + [" ", "Subtotal"])
        tablewriter.writerow([" "] + ("Total New "*max_width).split())
        row_height = 0
        total = 0
        for row in combined_table:
            subtotal = 0
            for j in row[::2]:
                subtotal += j
            tablewriter.writerow([row_height] + row + [subtotal])
            row_height += 1
            total += subtotal
        tablewriter.writerow(["Total:", total])
   