"""
Using the headers of the messages of the threads, this module is used for generating the following statistics can be
helpful in understanding the nature of the discussion threads:
* Distribution of the length (in units of time) of each discussion thread. Since one discussion thread has one
length, we have a distribution of these lengths.
* Distribution of inter-arrival times between the consecutive messages in all discussion threads. This information
would help in determining a possible termination of a discussion thread. If there is no activity on a thread beyond a
reasonable limit (can be mean + 2*S.D), then we can conclude the discussion thread to be dead.
Both these distributions can then be plotted as cumulative distribution functions (CDFs) using the CSV files generated
by this module.
"""
import json
from util.read_utils import *
import os.path


def thread_length_distribution(discussion_graph, foldername):
    if not os.path.exists(foldername):
        os.makedirs(foldername)
    thread_lengths = list()
    for conn_subgraph in nx.weakly_connected_component_subgraphs(discussion_graph):
        time_list = list()
        time_list = [datetime.datetime.strptime(x , "%a, %d %b %Y %H:%M:%S %z")
                     for x in nx.get_node_attributes(conn_subgraph, 'time').values()]
        current_thread_length = (max(time_list) - min(time_list)).total_seconds()
        thread_lengths.append((min(conn_subgraph.nodes()), current_thread_length))
    with open(foldername+"conversation_length.csv", mode='w') as dist_file:
        for node, current_thread_length in thread_lengths:
            dist_file.write("{0};{1}\n".format(node, current_thread_length))
            # dist_file.write("{0}\n".format(node, current_thread_length))
        dist_file.close()
    # thread_lengths = [x for (y, x) in thread_lengths]
    # thread_lengths.sort()
    # print("95th Percentile Thread Length:", thread_lengths[95*len(thread_lengths)//100], "secs.",
    #       "or", thread_lengths[95*len(thread_lengths)//100]/3600, "hrs.")
    # print("99th Percentile Thread Length:", thread_lengths[99*len(thread_lengths)//100], "secs.",
    #       "or", thread_lengths[99*len(thread_lengths)//100]/3600, "hrs.")
    # return thread_lengths


def message_inter_arrival_times(discussion_graph, json_data, foldername):
    if not os.path.exists(foldername):
        os.makedirs(foldername)
    with open(foldername+"response_time.csv", mode='w') as dist_file:
        for src, dstn in discussion_graph.edges():
            dist_file.write("{0};{1};{2}\n".format(src, dstn,
                            abs(get_datetime_object(json_data[src]['Time']) - get_datetime_object(json_data[dstn]['Time'])).total_seconds()))
            # dist_file.write("{0}\n".format(abs((json_data[str(src)]['Time'] - json_data[str(dstn)]['Time']).total_seconds())))
        dist_file.close()


def generate_time_stats_threads(nodelist_filename, edgelist_filename, clean_headers_filename, foldername, time_lbound=None, time_ubound=None):
    # Time limit can be specified as a parameter in the form of a timestamp in one of the identifiable formats and all
    # messages that have arrived before/after this timestamp will be ignored.

    # If true, then messages that belong to threads that have only a single author are ignored.
    ignore_lat = False
    discussion_graph = nx.DiGraph()
    json_data = dict()

    if time_ubound is None:
        time_ubound = time.strftime("%a, %d %b %Y %H:%M:%S %z")
    time_ubound = get_datetime_object(time_ubound)

    if time_lbound is None:
        time_lbound = time.strftime("%a, %d %b %Y %H:%M:%S %z")
    msgs_in_range = set()
    time_lbound = get_datetime_object(time_lbound)

    print("All messages before", time_ubound, "and after", time_lbound, "are being considered.")
    discussion_graph = nx.DiGraph()
    email_re = re.compile(r'[\w\.-]+@[\w\.-]+')

    # Add nodes into NetworkX graph by reading from CSV file
    if not ignore_lat:
        with open(nodelist_filename, "r") as node_file:
            for pair in node_file:
                node = pair.split(';', 2)
                if time_lbound <= get_datetime_object(node[2].strip()) < time_ubound:
                    node[0] = int(node[0])
                    msgs_in_range.add(node[0])
                    from_addr = email_re.search(node[1].strip())
                    from_addr = from_addr.group(0) if from_addr is not None else node[1].strip()
                    discussion_graph.add_node(node[0], time=node[2].strip(), sender=from_addr)
            node_file.close()
        print("Nodes added.")

        # Add edges into NetworkX graph by reading from CSV file
        with open(edgelist_filename, "r") as edge_file:
            for pair in edge_file:
                edge = pair.split(';')
                edge[0] = int(edge[0])
                edge[1] = int(edge[1])
                if edge[0] in msgs_in_range and edge[1] in msgs_in_range:
                    discussion_graph.add_edge(*edge)
            edge_file.close()
        print("Edges added.")

    else:
        lone_author_threads = get_lone_author_threads(save_file=None, nodelist_filename=nodelist_filename, edgelist_filename=edgelist_filename)
        # Add nodes into NetworkX graph only if they are not a part of a thread that has only a single author
        with open(nodelist_filename, "r") as node_file:
            for pair in node_file:
                node = pair.split(';', 2)
                node[0] = int(node[0])
                if time_lbound <= get_datetime_object(node[2].strip()) < time_ubound and node[0] not in lone_author_threads:
                    msgs_in_range.add(node[0])
                    from_addr = email_re.search(node[1].strip())
                    from_addr = from_addr.group(0) if from_addr is not None else node[1].strip()
                    discussion_graph.add_node(node[0], time=node[2].strip(), color="#ffffff", style='bold', sender=from_addr)
            node_file.close()
        print("Nodes added.")

    if len(msgs_in_range) == 0:
        return "No messages!"

    # Add edges into NetworkX graph only if they are not a part of a thread that has only a single author
    if ignore_lat:
        with open(edgelist_filename, "r") as edge_file:
            for pair in edge_file:
                edge = pair.split(';')
                edge[0] = int(edge[0])
                edge[1] = int(edge[1])
                if edge[0] not in lone_author_threads and edge[1] not in lone_author_threads:
                    if edge[0] in msgs_in_range and edge[1] in msgs_in_range:
                        discussion_graph.add_edge(*edge)
            edge_file.close()
        print("Edges added.")
    else:
        with open(edgelist_filename, "r") as edge_file:
            for pair in edge_file:
                edge = pair.split(';')
                edge[0] = int(edge[0])
                edge[1] = int(edge[1])
                if edge[0] in msgs_in_range and edge[1] in msgs_in_range:
                    discussion_graph.add_edge(*edge)
            edge_file.close()
        print("Edges added.")

    with open(clean_headers_filename, 'r') as json_file:
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
    if len(discussion_graph.edges()) == 0:
        return "No messages"
    thread_length_distribution(discussion_graph, foldername)
    message_inter_arrival_times(discussion_graph, json_data, foldername)
    return None


