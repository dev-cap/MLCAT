import json, numpy as np
from util.read_utils import *
import matplotlib.pyplot as plt


def generate_hyperedge_distribution(nodelist_filename, edgelist_filename, clean_headers_filename, foldername, time_limit=None, ignore_lat=False):
    """

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

