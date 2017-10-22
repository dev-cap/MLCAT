"""
This module is used to generate graphs that show the interaction between authors either through multiple edges or
through edge weights. There is an edge from one author to another if the former sent a message to the latter. These
graphs depict thread-wise interaction of the authors for the entire mailing list and these interactions are labelled
in chronological order to help identify the flow of messages across authors.
"""
import json
from util.read import *


def add_to_multigraph(graph_obj, discussion_graph, json_data, nbunch, label_prefix=''):
    """
    Add multiple edges to the MultiDiGraph object recursively.

    :param graph_obj: Object for a directed graph with mulitple edges.
    :param discussion_graph: A directed graph constructed from nodes and edges csv files.
    :param json_data: JSON header file.
    :param nbunch: A container of nodes. The container will be iterated through once.
    :param label_prefix: Chronological prefixes.
    """
    i = 0
    for node in sorted(nbunch):
        node_attr = json_data[node]
        if node_attr['Cc'] is None:
            addr_list = node_attr['To']
        else:
            addr_list = node_attr['To'] | node_attr['Cc']
        for to_address in addr_list:
            graph_obj.add_edge(node_attr['From'], to_address, label=label_prefix+str(i))
        succ_nbunch = [int(x) for x in discussion_graph.successors(node)]
        if succ_nbunch is not None:
            add_to_multigraph(graph_obj, discussion_graph, json_data, succ_nbunch, label_prefix+str(i)+'.')
        i += 1


def author_interaction_multigraph(discussion_graph, json_data, limit=10):
    """
    Generate graphs in PNG format to show author interaction through multiple edges.

    :param discussion_graph: A directed graph constructed from nodes and edges csv files.
    :param json_data: JSON header file.
    :param limit: Number of connected subgraphs to be considered.
    """
    niter = 0
    for conn_subgraph in nx.weakly_connected_component_subgraphs(discussion_graph):
        interaction_graph = nx.MultiDiGraph()
        origin = min(int(x) for x in conn_subgraph.nodes())
        add_to_multigraph(interaction_graph, discussion_graph, json_data, [origin])
        # print(json_data[origin])
        g1 = nx.to_agraph(interaction_graph)
        g1.draw("author_multi/"+str(origin)+'.png', prog='circo')
        niter += 1
        if limit == niter and limit > 0:
            break


def add_to_weighted_graph(graph_obj, discussion_graph, json_data, nbunch, node_enum=list()):
    """
    Add weighted edges to the DiGraph object recursively.

    :param graph_obj: Object for a directed graph with mulitple edges.
    :param discussion_graph: A directed graph constructed from nodes and edges csv files.
    :param json_data: JSON header file.
    :param nbunch: A container of nodes. The container will be iterated through once.
    :param node_enum: Enumerator to store unique senders and receipents.
    """
    for node in sorted(nbunch):
        node_attr = json_data[node]
        if node_attr['Cc'] is None:
            addr_list = node_attr['To']
        else:
            addr_list = node_attr['To'] | node_attr['Cc']
        if node_attr['From'] not in node_enum:
            node_enum.append(node_attr['From'])
        from_node = node_enum.index(node_attr['From'])
        for to_address in addr_list:
            if to_address not in node_enum:
                node_enum.append(to_address)
            to_node = node_enum.index(to_address)
            if not graph_obj.has_edge(from_node, to_node):
                graph_obj.add_edge(from_node, to_node, label=1)
            else:
                graph_obj[from_node][to_node]['label'] += 1
        succ_nbunch = [int(x) for x in discussion_graph.successors(node)]
        if succ_nbunch is not None:
            add_to_weighted_graph(graph_obj, discussion_graph, json_data, succ_nbunch, node_enum)


def author_interaction_weighted_graph(discussion_graph, json_data, limit=10):
    """
    Generate graphs in PNG format to show author interaction through weighted edges.

    :param discussion_graph: A directed graph constructed from nodes and edges csv files.
    :param json_data: JSON header file.
    :param limit: Number of connected subgraphs to be considered.
    """
    niter = 0
    for conn_subgraph in nx.weakly_connected_component_subgraphs(discussion_graph):
        interaction_graph = nx.DiGraph()
        origin = min(int(x) for x in conn_subgraph.nodes())
        add_to_weighted_graph(interaction_graph, discussion_graph, json_data, [origin], [])
        # print(json_data[origin])
        g1 = nx.to_agraph(interaction_graph)
        g1.draw("author_weighted/"+str(origin)+'.png', prog='circo')
        niter += 1
        if limit == niter and limit > 0:
            break


def weighted_multigraph():
    """

    Calls other functions to generate graphs that show the interaction between authors either through multiple edges or
    through edge weights.
    """
    # Time limit can be specified here in the form of a timestamp in one of the identifiable formats and all messages
    # that have arrived after this timestamp will be ignored.
    time_limit = None
    # If true, then messages that belong to threads that have only a single author are ignored.
    ignore_lat = True

    if time_limit is None:
        time_limit = time.strftime("%a, %d %b %Y %H:%M:%S %z")
    msgs_before_time = set()
    time_limit = get_datetime_object(time_limit)
    print("All messages before", time_limit, "are being considered.")

    discussion_graph = nx.DiGraph()
    email_re = re.compile(r'[\w\.-]+@[\w\.-]+')
    json_data = dict()

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

    with open('clean_data.json', 'r') as json_file:
        for chunk in lines_per_n(json_file, 9):
            json_obj = json.loads(chunk)
            # print("\nFrom", json_obj['From'], "\nTo", json_obj['To'], "\nCc", json_obj['Cc'])
            from_addr = email_re.search(json_obj['From'])
            json_obj['From'] = from_addr.group(0) if from_addr is not None else json_obj['From']
            json_obj['To'] = set(email_re.findall(json_obj['To']))
            json_obj['Cc'] = set(email_re.findall(json_obj['Cc'])) if json_obj['Cc'] is not None else None
            # print("\nFrom", json_obj['From'], "\nTo", json_obj['To'], "\nCc", json_obj['Cc'])
            json_data[json_obj['Message-ID']] = json_obj
    print("JSON data loaded.")

    author_interaction_weighted_graph(discussion_graph, json_data, limit=20)
    author_interaction_multigraph(discussion_graph, json_data, limit=20)

