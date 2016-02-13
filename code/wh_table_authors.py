import networkx as nx
import csv


def generate_wh_table_authors():
    # TODO: Generate the table for a given time interval passed as a parameter.
    discussion_graph = nx.DiGraph()

    # Add nodes into NetworkX graph by reading CSV files
    with open("graph_nodes.csv", "r") as node_file:
        for pair in node_file:
            node = pair.split(';', 2)
            discussion_graph.add_node(int(node[0]), time=node[2].strip(), color="#ffffff", style='bold', sender=node[1].strip())
        node_file.close()
    print("Nodes added.")

    # Add edges into NetworkX graph by reading CSV files
    with open("graph_edges.csv", "r") as edge_file:
        for pair in edge_file:
            edge = pair.split(';')
            edge[0] = int(edge[0])
            edge[1] = int(edge[1])
            try:
                discussion_graph.node[edge[0]]['sender']
                discussion_graph.node[edge[1]]['sender']
                discussion_graph.add_edge(*edge)
            except KeyError:
                pass
        edge_file.close()
    print("Edges added.")

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
            node_height = nx.shortest_path_length(conn_subgraph, source_node, node)
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

    # for row in wh_table:
    #     print(row[:max_width+1])
    # print()
    # for row in new_wh_table:
    #     print(row[:max_width+1])

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

    with open('wh_table_authors.csv', 'w') as csvfile:
        tablewriter = csv.writer(csvfile)
        # tablewriter.writerow(["No. of threads with a total of 'i' authors at a height 'h':"])
        # tablewriter.writerow(["Height(h)", "Number of authors(i)"])
        # tablewriter.writerow([" "] + list(range(1, max_width + 1)) + ["Subtotal"])
        # row_height = 0
        # total = 0
        # for row in wh_table:
        #     row = row[1:max_width+1]
        #     subtotal = 0
        #     for j in row:
        #         subtotal += j
        #     tablewriter.writerow([row_height] + row + [subtotal])
        #     row_height += 1
        #     total += subtotal
        # tablewriter.writerow(["Total:", total])
        # tablewriter.writerow([" "])
        # tablewriter.writerow(["No. of threads with a total of 'i' authors at a height 'h':"])
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
        csvfile.close()

generate_wh_table_authors()