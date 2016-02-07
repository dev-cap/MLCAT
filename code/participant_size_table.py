import networkx as nx
import csv


def generate_participant_size_table():
    # TODO: Generate the table for a given time interval passed as a parameter.
    discussion_graph = nx.DiGraph()

    # Add nodes into NetworkX graph by reading CSV files
    with open("graph_nodes.csv", "r") as node_file:
        for pair in node_file:
            node = pair.split(';', 2)
            discussion_graph.add_node(node[0], time=node[2].strip(), color="#ffffff", style='bold', sender=node[1].strip())
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