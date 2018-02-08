"""
This module uses Graph-Tool.clustering package to count the occurrence of motifs (which are k-size node-induced
subgraphs) and consequently obtain the motif significance profile, for subgraphs with k vertices. Then tuples with
three lists are written to a text file: the list of motifs found, the list with their respective counts, and their
respective z-scores.
"""
import json
from graph_tool.all import *
from util.read import *


def detect_motifs(directed_graph, min_size, max_size):
    """
    This method detects motifs of a range of sizes in the specified graph.
    :param directed_graph: The directed graph for which motifs have to be found.
    :param min_size: Minimum size of the motifs to be detected (inclusive)
    :param max_size: Maximum size of the motifs to be detected (exclusive)
    """
    for motif_size in range(min_size, max_size):
        print("Detecting network motifs of size %d..." %(motif_size))
        """
        Count the occurrence of k-size node-induced subgraphs (motifs). A tuple with two lists is returned: the list of
        motifs found (grouped according to their isomorphism class and sorted according to in-degree sequence, out-degree
        sequence, and number of edges) and the list with their respective counts.
        """
        motif_list, counts = motifs(directed_graph, motif_size)
        counts = [(x, None) for x in counts]
        motif_profile = dict(zip(motifs, counts))
        motif_list, zscores = motif_significance(directed_graph, motif_size, self_loops = True, motif_list = motif_list)
        for index in range(len(motif_list)):
            motif = motif_list[index]
            motif_profile[motif] = (motif_profile[motif][0], zscores[index])
        with open("motifs/" + "motif_" + str(motif_size) + ".txt", 'w') as output_file:
            output_file.write(str(motif_profile))
            output_file.close()


author_graph = Graph(directed=True)
# author_graph.es["weight"] = 1.0
json_data = dict()
author_map = dict()
email_re = re.compile(r'[\w\.-]+@[\w\.-]+')

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

if not ignore_lat:
    with open('clean_data.json', 'r') as json_file:
        for chunk in lines_per_n(json_file, 9):
            json_obj = json.loads(chunk)
            json_obj['Message-ID'] = int(json_obj['Message-ID'])
            json_obj['Time'] = datetime.datetime.strptime(json_obj['Time'], "%a, %d %b %Y %H:%M:%S %z")
            if json_obj['Time'] < time_limit:
                # print("\nFrom", json_obj['From'], "\nTo", json_obj['To'], "\nCc", json_obj['Cc'])
                from_addr = email_re.search(json_obj['From'])
                json_obj['From'] = from_addr.group(0) if from_addr is not None else json_obj['From']
                json_obj['To'] = set(email_re.findall(json_obj['To']))
                json_obj['Cc'] = set(email_re.findall(json_obj['Cc'])) if json_obj['Cc'] is not None else None
                # print("\nFrom", json_obj['From'], "\nTo", json_obj['To'], "\nCc", json_obj['Cc'])
                json_data[json_obj['Message-ID']] = json_obj
    print("JSON data loaded.")
else:
    lone_author_threads = get_lone_author_threads(False)
    with open('clean_data.json', 'r') as json_file:
        for chunk in lines_per_n(json_file, 9):
            json_obj = json.loads(chunk)
            json_obj['Message-ID'] = int(json_obj['Message-ID'])
            if json_obj['Message-ID'] not in lone_author_threads:
                json_obj['Time'] = datetime.datetime.strptime(json_obj['Time'], "%a, %d %b %Y %H:%M:%S %z")
                if json_obj['Time'] < time_limit:
                    # print("\nFrom", json_obj['From'], "\nTo", json_obj['To'], "\nCc", json_obj['Cc'])
                    from_addr = email_re.search(json_obj['From'])
                    json_obj['From'] = from_addr.group(0) if from_addr is not None else json_obj['From']
                    json_obj['To'] = set(email_re.findall(json_obj['To']))
                    json_obj['Cc'] = set(email_re.findall(json_obj['Cc'])) if json_obj['Cc'] is not None else None
                    # print("\nFrom", json_obj['From'], "\nTo", json_obj['To'], "\nCc", json_obj['Cc'])
                    json_data[json_obj['Message-ID']] = json_obj
    print("JSON data loaded.")

"""
A vertex can be added with the add_vertex() method, which returns an instance of a Vertex class. The add_vertex()
method also accepts an optional parameter which specifies the number of vertices to create. If this value is greater
than 1, it returns an iterator on the added vertex descriptors. Each vertex in a graph has an unique index, which is
always between 0 and N-1, where N is the number of vertices. This index can be obtained by using the vertex_index
attribute of the graph or by converting the vertex descriptor to an int. Since vertices are uniquely identifiable by
their indexes, one can obtain the descriptor of a vertex with a given index using the vertex() method which takes an
index, and returns a vertex descriptor.

Edges can be added by calling the add_edge() method, which returns an instance of the Edge class. Edge descriptors
have two useful methods, source() and target(), which return the source and target vertex of an edge. Edges cannot be
directly obtained by its index, but if the source and target vertices of a given edge is known, it can be obtained
with the edge() method.
"""

index = 0
for id, node in json_data.items():
    if node['From'] not in author_map:
        author_map[node['From']] = index
        author_graph.add_vertex()
        index += 1
    for to_addr in node['To']:
        if to_addr not in author_map:
            author_map[to_addr] = index
            author_graph.add_vertex()
            index += 1
        author_graph.add_edge(author_map[node['From']], author_map[to_addr])

    if node['Cc'] is None:
        continue
    for to_addr in node['Cc']:
        if to_addr not in author_map:
            author_map[to_addr] = index
            author_graph.add_vertex()
            index += 1
        author_graph.add_edge(author_map[node['From']], author_map[to_addr])

detect_motifs(author_graph, 4, 21)