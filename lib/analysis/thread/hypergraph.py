"""
This module is used to model each discussion thread as one hypergraph. All the email header information can be
represented as one hyperedge of a hypergraph. This concise format for representing a discussion thread as a
hypergraph is then stored as a table to a CSV file, with the author column headers containing the ids of the authors.
All the author columns are sorted left to right in the descending order of out degree, followed by in degree. The
authors identified in this discussion thread are indexed in a separate file using the author_uid_map.py.
"""
from util.read import *
import matplotlib.pyplot as plt
import networkx as nx
import json
import re
import csv


class MessageNode:
    """
    Models message information as a message node.

    :param msg_id: Unique message id.
    :param height: Height at which the node is present.
    :param parent_id: Id of the parent node.
    :param time: Time at which the message was sent.
    :param from_addr: Message author.
    :param to_addr: Message receiver.
    :param cc_addr: Message recever.
    """
    def __init__(self, msg_id=0, height=-1, parent_id=0, time=None, from_addr=None, to_addr=None, cc_addr=None):
        """

        :param msg_id: Unique message id.
        :param height: Height at which the node is present.
        :param parent_id: Id of the parent node.
        :param time: Time at which the message was sent.
        :param from_addr: Message author.
        :param to_addr: Message receiver.
        :param cc_addr: Message recever.
        """
        self.msg_id = msg_id
        self.height = height
        self.parent_id = parent_id
        self.time = time
        self.from_addr = from_addr
        self.to_addr = to_addr
        self.cc_addr = cc_addr

    def __lt__(self,other):
        return (self.height < other.height) if (self.height != other.height) else (self.msg_id < other.msg_id)


def add_thread_nodes(thread_authors, nbunch, parent_id, curr_height, json_data, thread_nodes, conn_subgraph):
    """
    Adds thread nodes of type MessageNode and thread authors recursively from the JSON data.

    :param thread_authors: A set to store author threads.
    :param nbunch: Stores nodes and contains the origin node initially.
    :param parent_id: Parent ID of each node, None initially.
    :param curr_height: Indicates the height of the current node, 0 when the function is called.
    :param json_data: The JSON data used to extract the thread attributes.
    :param thread_nodes: A list containing the nodes of type MessageNode.
    :param conn_subgraph: Weakly connected component subgraph from the discussion graph.
    """
    for node in nbunch:
        next_nbunch = list()
        node_attr = json_data[int(node)]
        thread_nodes.append(MessageNode(node_attr['Message-ID'], curr_height, parent_id, node_attr['Time'],
                                        node_attr['From'], node_attr['To'], node_attr['Cc']))
        thread_authors.add(node_attr['From'])
        thread_authors |= node_attr['To']
        if node_attr['Cc']:
            thread_authors |= node_attr['Cc']
        next_nbunch.extend(conn_subgraph.successors(str(node)))
        add_thread_nodes(thread_authors, next_nbunch, node, curr_height + 1, json_data, thread_nodes, conn_subgraph)


def generate_hyperedges():
    """

    Generates hyperedges from the discussion graph obtained from the nodes and edges stored in graph_nodes.csv and graph_edges.csv.
    All email header information can be represented as one hyperedge of a hypergraph.
    """
    discussion_graph = nx.DiGraph()
    json_data = dict()
    email_re = re.compile(r'[\w\.-]+@[\w\.-]+')

    with open("graph_nodes.csv", "r") as node_file:
        for pair in node_file:
            node = pair.split(';', 2)
            discussion_graph.add_node(node[0], time=node[2].strip(), sender=node[1].strip())
        node_file.close()
    print("Nodes added.")

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

    with open('author_uid_map.json', 'r') as uid_file:
        author_uid = json.load(uid_file)
        uid_file.close()
    print("JSON data loaded.")

    for conn_subgraph in nx.weakly_connected_component_subgraphs(discussion_graph):
        origin_node = min(int(x) for x in conn_subgraph.nodes())
        if origin_node != 5141:
            continue
        thread_nodes = list()
        thread_authors = set()
        add_thread_nodes(thread_authors, [origin_node], None, 0, json_data, thread_nodes, conn_subgraph)
        thread_authors = list(thread_authors)
        thread_nodes.sort()

        index = 1
        author_interaction_matrix = [[' ' for x in range(len(thread_authors))] for y in range(1+len(thread_nodes))]
        for message_node in thread_nodes:
            # print(len(thread_authors), len(thread_nodes), thread_authors.index(message_node.from_addr), index)
            for to_addr in message_node.to_addr:
                author_interaction_matrix[index][thread_authors.index(to_addr)] = 'T'
            for cc_addr in message_node.cc_addr:
                author_interaction_matrix[index][thread_authors.index(cc_addr)] = 'C'
            author_interaction_matrix[index][thread_authors.index(message_node.from_addr)] = 'F'
            index += 1

        index = 0
        # author_enumeration = dict()
        for author in thread_authors:
            author_interaction_matrix[0][index] = "author-" + str(author_uid[author])
            index += 1
            # author_enumeration[author] = "author-" + str(author_uid[author])

        indegree = [0 for x in range(len(thread_authors))]
        outdegree = [0 for x in range(len(thread_authors))]
        for i in range(1, len(thread_nodes)+1):
            for j in range(len(thread_authors)):
                if author_interaction_matrix[i][j] in ('T', 'C'):
                    indegree[j] += 1
                elif author_interaction_matrix[i][j] == 'F':
                    outdegree[j] += 1

        thread_authors = [x for (y,x) in sorted(zip(outdegree, thread_authors), key=lambda pair: pair[0], reverse=True)]
        indegree = [x for (y,x) in sorted(zip(outdegree,indegree), key=lambda pair: pair[0], reverse=True)]
        author_interaction_matrix = map(list, zip(*author_interaction_matrix))
        author_interaction_matrix = [x for (y,x) in sorted(zip(outdegree, author_interaction_matrix), key=lambda pair: pair[0], reverse=True)]
        author_interaction_matrix = list(map(list, zip(*author_interaction_matrix)))
        outdegree.sort(reverse=True)

        index = 1
        prev_height = -1
        total_cc = row_cc = 0
        total_to = row_to = 0
        with open("hyperedge/" + str(origin_node) + ".csv", 'w') as hyperedge_file:
            tablewriter = csv.writer(hyperedge_file)
            tablewriter.writerow(["Height", "Message-ID", "Parent-ID", "Time"]
                                 + author_interaction_matrix[0] + ["No. of CCs", "No. of TOs"])
            for message_node in thread_nodes:
                curr_height = " " if message_node.height == prev_height else message_node.height
                parent_id = message_node.parent_id if message_node.parent_id else "None"
                row_cc = author_interaction_matrix[index].count('C')
                row_to = author_interaction_matrix[index].count('T')
                total_cc += row_cc
                total_to += row_to
                tablewriter.writerow([curr_height, message_node.msg_id, parent_id, message_node.time]
                                 + author_interaction_matrix[index] + [row_cc, row_to])
                prev_height = message_node.height
                index += 1
            tablewriter.writerow([" ", " ", " ", "Outdegree"] + outdegree + ["Total CCs", "Total TOs"])
            tablewriter.writerow([" ", " ", " ", "Indegree"] + indegree + [total_cc, total_to])
            hyperedge_file.close()


def generate_hyperedge_distribution(nodelist_filename, edgelist_filename, clean_headers_filename, foldername, time_limit=None, ignore_lat=False):
    """
    Generate the distribution of hyperedges for messages in a certain time limit, stores it as hyperedge_distribution.csv based on edge frequency and generates a diagram stored in plots.

    :param nodelist_filename: The csv file containing the nodes.
    :param edgelist_filename: The csv file containing the edges.
    :param clean_headers_filename: The JSON file containing the cleaned headers.
    :param foldername: The mailbox folder.
    :param ignore_lat: If true, then messages that belong to threads that have only a single author are ignored.
    :param time_limit: Time limit can be specified here in the form of a timestamp in one of the identifiable formats
            and all messages that have arrived after this timestamp will be ignored.
    """
    if time_limit is None:
        time_limit = time.strftime("%a, %d %b %Y %H:%M:%S %z")
    msgs_before_time = set()
    time_limit = get_datetime_object(time_limit)
    print("All messages before", time_limit, "are being considered.")

    discussion_graph = nx.DiGraph()
    email_re = re.compile(r'[\w\.-]+@[\w\.-]+')
    json_data = dict()
    # Author participation denotes the the number of threads an author is active in. This is a dictionary keyed
    # by the author's email id with the value equalling the number of threads in which the author has sent a mail.
    author_participation = dict()

    # Add nodes into NetworkX graph by reading from CSV file
    if not ignore_lat:
        with open(nodelist_filename, "r") as node_file:
            for pair in node_file:
                node = pair.split(';')
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
        lone_author_threads = get_lone_author_threads(save_file=None, nodelist_filename=nodelist_filename, edgelist_filename=edgelist_filename)
        # Add nodes into NetworkX graph only if they are not a part of a thread that has only a single author
        with open(nodelist_filename, "r") as node_file:
            for pair in node_file:
                node = pair.split(';')
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

    with open(clean_headers_filename, 'r') as json_file:
        for chunk in lines_per_n(json_file, 9):
            json_obj = json.loads(chunk)
            # print("\nFrom", json_obj['From'], "\nTo", json_obj['To'], "\nCc", json_obj['Cc'])
            from_addr = email_re.search(json_obj['From'])
            json_obj['From'] = from_addr.group(0) if from_addr is not None else json_obj['From']
            author_participation[json_obj['From']] = 0
            json_obj['To'] = set(email_re.findall(json_obj['To']))
            json_obj['Cc'] = set(email_re.findall(json_obj['Cc'])) if json_obj['Cc'] is not None else None
            for email_id in json_obj['To']:
                author_participation[email_id] = 0
            if json_obj['Cc'] is not None:
                for email_id in json_obj['Cc']:
                    author_participation[email_id] = 0
            json_data[json_obj['Message-ID']] = json_obj
    print("JSON data loaded.")

    # The index of the hyperedge_dist list contains the number of vertices receiving the hyperedge and the value stored
    # at the index corresponds to the frequency or the number of observations.
    hyperedge_dist = [0 for x in range(1000)]
    max_len = -1
    for conn_subgraph in nx.weakly_connected_component_subgraphs(discussion_graph):
        authors_active = set()
        for msg_id in conn_subgraph.nodes():
            msg_attr = json_data[msg_id]
            if msg_attr['From'] not in authors_active:
                author_participation[msg_attr['From']] += 1
            if msg_attr['Cc'] is not None:
                curr_len = len(msg_attr['Cc']) + len(msg_attr['To'])
            else:
                curr_len = len(msg_attr['To'])
            hyperedge_dist[curr_len] += 1
            if curr_len > max_len:
                max_len = curr_len

    with open(foldername+"/tables/hyperedge_distribution.csv", 'w') as hyperedge_dist_file:
        hyperedge_dist_file.write("No. of Vertices Receiving Hyperedge,Frequency\n")
        for index in range(1, 1000):
            hyperedge_dist_file.write(str(index) + "," + str(hyperedge_dist[index]) + "\n")
            if index == max_len:
                break
    hyperedge_dist_file.close()
    print("Hyperedge distribution statistic written to file.")

    plt.clf()
    plt.plot(range(1, max_len+1), hyperedge_dist[1:max_len+1])
    plt.savefig(foldername+"/plots/hyperedge_distribution.png")

    with open(foldername+"/tables/author_thread_participation.csv", 'w') as author_participation_file:
        author_participation_file.write("Author Email ID,Number of Active Threads\n")
        for author_id, num_threads in author_participation.items():
            author_participation_file.write(author_id + "," + str(num_threads) + "\n")
    print("Author-Thread Participation statistic written to file.")

    plt.clf()
    data = [num_threads for author_id, num_threads in author_participation.items()]
    plt.hist(data, bins=50)
    plt.savefig(foldername+"/plots/author_thread_participation.png")

