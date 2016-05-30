"""
This module is used to find the community structure of the network according to the Infomap method of Martin Rosvall
and Carl T. Bergstrom and returns an appropriate VertexClustering object. This module has been implemented using both
the iGraph package and the Infomap tool from MapEquation.org. The VertexClustering object represents the clustering of
the vertex set of a graph and also provides some methods for getting the subgraph corresponding to a cluster and such.

"""
import re
import json
import igraph
from util.read_utils import lines_per_n


author_graph = igraph.Graph()
author_graph.es["weight"] = 1.0
json_data = dict()
author_map = dict()
email_re = re.compile(r'[\w\.-]+@[\w\.-]+')

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
        author_graph.add_vertex(name=node['From'])
        index += 1
    for to_addr in node['To']:
        if to_addr not in author_map:
            author_map[to_addr] = index
            author_graph.add_vertex(name=to_addr)
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
            author_graph.add_vertex(name=to_addr)
            index += 1
        if author_graph[node['From'], to_addr] == 0:
            author_graph.add_edge(node['From'], to_addr, weight=1)
        else:
            author_graph[node['From'], to_addr] += 1

print("Nodes and Edges added to iGraph.")
vertex_clustering_obj = author_graph.community_infomap(edge_weights=author_graph.es["weight"])
with open("community_vertex_clustering.txt", 'w') as output_file:
    output_file.write(str(vertex_clustering_obj))
    output_file.close()
