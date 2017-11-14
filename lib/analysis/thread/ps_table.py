import csv
from util.read import *
import networkx as nx


def generate(ignore_lat=False, time_limit=None):
    """

    This function generate a table containing the number of mails in a thread and the corresponding aggregate count
    of the number of threads that have that number of mails in them, along with the total number of authors who have
    participated in such threads and the average number of authors. This table is then written to a CSV file.

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
        with open("graph_nodes.csv", "r") as node_file:
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
        with open("graph_edges.csv", "r") as edge_file:
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
        with open("graph_nodes.csv", "r") as node_file:
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
        with open("graph_edges.csv", "r") as edge_file:
            for pair in edge_file:
                edge = pair.split(';')
                edge[0] = int(edge[0])
                edge[1] = int(edge[1])
                if edge[0] not in lone_author_threads and edge[1] not in lone_author_threads:
                    if edge[0] in msgs_before_time and edge[1] in msgs_before_time:
                        discussion_graph.add_edge(*edge)
            edge_file.close()
        print("Edges added.")

    max_nodes = max(nx.number_of_nodes(i) for i in nx.weakly_connected_component_subgraphs(discussion_graph))
    print("Maximum number of mails in a thread:", max_nodes)

    # This list stores the number of authors in all threads of a given size. If no_of_authors[i] = k, there are a total
    # of k authors in all threads of size i.
    no_of_authors = [0 for x in range(max_nodes+1)]
    no_of_threads = [0 for x in range(max_nodes+1)]
    
    for conn_subgraph in nx.weakly_connected_component_subgraphs(discussion_graph):
        authors = set()
        for node, attributes in conn_subgraph.nodes_iter(data=True):
            authors.add(attributes['sender'])
        no_of_authors[nx.number_of_nodes(conn_subgraph)] += len(authors)
        no_of_threads[nx.number_of_nodes(conn_subgraph)] += 1

    # print(no_of_authors)
    with open('participant_size_table.csv', 'w') as csvfile:
        tablewriter = csv.writer(csvfile)
        nmails = 0
        tablewriter.writerow(["No. of mails", "No. of threads", "Total no. of authors", "Average no. of authors"])
        for row1 in no_of_authors:
            if row1 != 0:
                row2 = no_of_threads[nmails]
                tablewriter.writerow([nmails, row2, row1, format(round(row1/row2, 3), '.3f')])
            nmails += 1
        csvfile.close()
