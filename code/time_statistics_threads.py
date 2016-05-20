import networkx as nx
import json
from util.json_utils import lines_per_n
from datetime import *


def thread_length_distribution(discussion_graph):
    thread_lengths = list()
    for conn_subgraph in nx.weakly_connected_component_subgraphs(discussion_graph):
        time_list = list()
        for node in conn_subgraph.nodes():
            time_list = [datetime.strptime(x , "%a, %d %b %Y %H:%M:%S %z")
                         for x in nx.get_node_attributes(conn_subgraph, 'time').values()]
        current_thread_length = (max(time_list) - min(time_list)).total_seconds()
        thread_lengths.append((min([int(x) for x in conn_subgraph.nodes()]), current_thread_length))
    with open("thread_length_distribution.csv", mode='w') as dist_file:
        for node, current_thread_length in thread_lengths:
            dist_file.write("{0};{1}\n".format(node, current_thread_length))
        dist_file.close()
    thread_lengths = [x for (y, x) in thread_lengths if x > 0]
    thread_lengths.sort()
    print("95th Percentile Thread Length:", thread_lengths[95*len(thread_lengths)//100], "secs.")
    print("99th Percentile Thread Length:", thread_lengths[99*len(thread_lengths)//100], "secs.")
    return thread_lengths


def message_inter_arrival_times(discussion_graph, json_data):
    with open("thread_inter_arrival_times.csv", mode='w') as dist_file:
        for src, dstn in discussion_graph.edges():
            dist_file.write("{0};{1};{2}\n".format(src, dstn,
                            abs((json_data[src]['Time'] - json_data[dstn]['Time']).total_seconds())))
        dist_file.close()

discussion_graph = nx.DiGraph()
json_data = dict()

with open("graph_nodes.csv", "r") as node_file:
    for pair in node_file:
        node = pair.split(';')
        discussion_graph.add_node(node[0], time=node[2].strip(),
                                  color='#'+(hex(hash(node[1].strip()))[-6:]).upper(),
                                  style='bold', sender=node[1].strip())
    node_file.close()
print("Nodes added.")

with open("graph_edges.csv", "r") as edge_file:
    for pair in edge_file:
        edge = pair.split(';')
        edge[1] = edge[1].strip()
        discussion_graph.add_edge(*edge)
    edge_file.close()
print("Edges added.")

with open('headers.json', 'r') as json_file:
    for chunk in lines_per_n(json_file, 9):
        json_obj = json.loads(chunk)
        json_obj['Time'] = datetime.strptime(json_obj['Time'], "%a, %d %b %Y %H:%M:%S %z")
        json_data[str(json_obj['Message-ID'])] = json_obj
print("JSON data loaded.")

thread_length_distribution(discussion_graph)
message_inter_arrival_times(discussion_graph, json_data)