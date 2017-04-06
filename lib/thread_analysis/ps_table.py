import csv
from util.read_utils import *
import networkx as nx


def generate_participant_size_table(ignore_lat=False, time_limit=None):
    """
    This function generate a table containing the number of mails in a thread and the corresponding aggregate count
    of the number of threads that have that number of mails in them, along with the total number of authors who have
    participated in such threads and the average number of authors. This table is then written to a CSV file.
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
    #call function in read_utils
    nodelist_filename="graph_nodes.csv"
    edgelist_filename="graph_edges.csv"
    add_elements_to_graph(ignore_lat, nodelist_filename, time_limit, msgs_before_time, email_re, edgelist_filename,
                          discussion_graph)

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

generate_participant_size_table()
