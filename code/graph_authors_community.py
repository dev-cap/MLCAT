"""
This module is used to find the community structure of the network according to the Infomap method of Martin Rosvall
and Carl T. Bergstrom and returns an appropriate VertexClustering object. This module has been implemented using both
the iGraph package and the Infomap tool from MapEquation.org. The VertexClustering object represents the clustering of
the vertex set of a graph and also provides some methods for getting the subgraph corresponding to a cluster and such.

"""
import json
import igraph
import cairo
from util.read_utils import *


author_graph = igraph.Graph()
author_graph.es["weight"] = 1.0
json_data = dict()
author_map = dict()
email_re = re.compile(r'[\w\.-]+@[\w\.-]+')

c_surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1600, 900)
ctx = cairo.Context(c_surface)
ctx.scale(1900, 900)
ctx.rectangle(0, 0, 1, 1)
ctx.set_source_rgba(0,0,0,0)
ctx.fill()

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
Graphs can also be indexed by strings or pairs of vertex indices or vertex names. When a graph is
indexed by a string, the operation translates to the retrieval, creation, modification or deletion
of a graph attribute.

When a graph is indexed by a pair of vertex indices or names, the graph itself is treated as an
adjacency matrix and the corresponding cell of the matrix is returned. Assigning values different
from zero or one to the adjacency matrix will be translated to one, unless the graph is weighted,
in which case the numbers will be treated as weights.
"""
index = 0
for id, node in json_data.items():
    if node['From'] not in author_map:
        author_map[node['From']] = index
        author_graph.add_vertex(name=node['From'], label=node['From'])
        index += 1
    for to_addr in node['To']:
        if to_addr not in author_map:
            author_map[to_addr] = index
            author_graph.add_vertex(name=to_addr, label=to_addr)
            index += 1
        if author_graph[node['From'], to_addr] == 0:
            author_graph.add_edge(node['From'], to_addr, weight=1)
        else:
            author_graph[node['From'], to_addr] += 1
    if node['Cc'] is None:
        continue
    for to_addr in node['Cc']:
        if to_addr not in author_map:
            author_map[to_addr] = index
            author_graph.add_vertex(name=to_addr, label=to_addr)
            index += 1
        if author_graph[node['From'], to_addr] == 0:
            author_graph.add_edge(node['From'], to_addr, weight=1)
        else:
            author_graph[node['From'], to_addr] += 1
    if index == 100:
        break
print("Nodes and Edges added to iGraph.")

vertex_dendogram = author_graph.community_edge_betweenness(clusters=8, directed=True, weights="weight")
igraph.plot(vertex_dendogram, "vd.pdf", vertex_label_size=3, bbox=(1200, 1200))

vertex_clustering_obj = author_graph.community_infomap(edge_weights=author_graph.es["weight"])
igraph.plot(vertex_clustering_obj, "vc.pdf", vertex_label_size=10, bbox=(1500, 1500))

with open("community_vertex_clustering.txt", 'w') as output_file:
    output_file.write(str(vertex_clustering_obj))
    output_file.close()
