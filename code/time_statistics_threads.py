import json
from util.read_utils import *


def thread_length_distribution(discussion_graph):
    thread_lengths = list()
    for conn_subgraph in nx.weakly_connected_component_subgraphs(discussion_graph):
        time_list = list()
        time_list = [datetime.datetime.strptime(x , "%a, %d %b %Y %H:%M:%S %z")
                     for x in nx.get_node_attributes(conn_subgraph, 'time').values()]
        current_thread_length = (max(time_list) - min(time_list)).total_seconds()
        thread_lengths.append((min(conn_subgraph.nodes()), current_thread_length))
    with open("thread_length_distribution.csv", mode='w') as dist_file:
        for node, current_thread_length in thread_lengths:
            dist_file.write("{0};{1}\n".format(node, current_thread_length))
        dist_file.close()
    thread_lengths = [x for (y, x) in thread_lengths]
    thread_lengths.sort()
    print("95th Percentile Thread Length:", thread_lengths[95*len(thread_lengths)//100], "secs.",
          "or", thread_lengths[95*len(thread_lengths)//100]/3600, "hrs.")
    print("99th Percentile Thread Length:", thread_lengths[99*len(thread_lengths)//100], "secs.",
          "or", thread_lengths[99*len(thread_lengths)//100]/3600, "hrs.")
    return thread_lengths


def message_inter_arrival_times(discussion_graph, json_data):
    with open("thread_inter_arrival_times.csv", mode='w') as dist_file:
        for src, dstn in discussion_graph.edges():
            dist_file.write("{0};{1};{2}\n".format(src, dstn,
                            abs((json_data[str(src)]['Time'] - json_data[str(dstn)]['Time']).total_seconds())))
        dist_file.close()


# Time limit can be specified here in the form of a timestamp in one of the identifiable formats and all messages
# that have arrived after this timestamp will be ignored.
time_limit = None
# If true, then messages that belong to threads that have only a single author are ignored.
ignore_lat = True
discussion_graph = nx.DiGraph()
json_data = dict()

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
                discussion_graph.add_node(node[0], time=node[2].strip(), sender=from_addr)
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
        json_obj['Time'] = datetime.datetime.strptime(json_obj['Time'], "%a, %d %b %Y %H:%M:%S %z")
        json_data[str(json_obj['Message-ID'])] = json_obj
print("JSON data loaded.")

thread_length_distribution(discussion_graph)
message_inter_arrival_times(discussion_graph, json_data)