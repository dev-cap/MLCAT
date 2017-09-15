"""
This module is used to find the community structure of the network according to the Infomap method of Martin Rosvall
and Carl T. Bergstrom and returns an appropriate VertexClustering object. This module has been implemented using both
the iGraph package and the Infomap tool from MapEquation.org. The VertexClustering object represents the clustering of
the vertex set of a graph and also provides some methods for getting the subgraph corresponding to a cluster and such.

"""
import json
import subprocess
import sys

import igraph
import numpy
import plotly
from matplotlib import pyplot as plt
from plotly.tools import FigureFactory as FF
from scipy.cluster.hierarchy import dendrogram, linkage

from analysis.author import generate_author_ranking
from util.read import *

sys.setrecursionlimit(10000)


def write_authors_data_matrix(json_data, tree_filename="infomap/output/"+"author_graph.tree"):
    """

    :param json_data:
    :return:
    """
    top_authors = set()
    top_authors_data = dict()
    author_scores = generate_author_ranking(active_score=2, passive_score=1, write_to_file=False)
    index = 0
    for email_addr, author_score in author_scores:
        index += 1
        top_authors.add(email_addr)
        top_authors_data[email_addr] = [author_score]
        if index == 100:
            break

    print("Adding nodes to author's graph...")
    author_graph = nx.DiGraph()
    for msg_id, message in json_data.items():
        if message['From'] in top_authors:
            if message['Cc'] is None:
                addr_list = message['To']
            else:
                addr_list = message['To'] | message['Cc']
            for to_address in addr_list:
                if to_address in top_authors:
                    if author_graph.has_edge(message['From'], to_address):
                        author_graph[message['From']][to_address]['weight'] *= \
                            author_graph[message['From']][to_address]['weight'] / (author_graph[message['From']][to_address]['weight'] + 1)
                    else:
                        author_graph.add_edge(message['From'], to_address, weight=1)

    author_graph_undirected = author_graph.to_undirected()
    clustering_coeff = nx.clustering(author_graph_undirected)
    in_degree_dict = author_graph.in_degree(nbunch=author_graph.nodes_iter())
    out_degree_dict = author_graph.out_degree(nbunch=author_graph.nodes_iter())

    for email_addr in top_authors:
        top_authors_data[email_addr].append(in_degree_dict[email_addr])
        top_authors_data[email_addr].append(out_degree_dict[email_addr])
        top_authors_data[email_addr].append(clustering_coeff[email_addr])

    print("Parsing", tree_filename + "...")
    with open(tree_filename, 'r') as tree_file:
        for line in tree_file:
            if not line or line[0] == '#':
                continue
            line = line.split()
            if line[2][1:-1] in top_authors:
                top_authors_data[line[2][1:-1]].append(float(line[1]))
        tree_file.close()

    with open("top_authors_data.csv", 'w') as output_file:
        output_file.write("Email Address,Author Score,In-Degree,Out-Degree,Clustering Coeff,Module Flow\n")
        for email_addr, data_list in top_authors_data.items():
            output_file.write(email_addr+","+",".join([str(x) for x in data_list])+"\n")
        output_file.close()
    print("Authors data written to file.")


def write_to_pajek(author_graph, filename="author_graph.net"):
    # Write Pajek file compatible with the Infomap Community Detection module
    nx.write_pajek(author_graph, filename)
    lines_in_file= list()
    with open(filename, 'r') as pajek_file:
        for line in pajek_file:
            lines_in_file.append(line)
    num_vertices = int(lines_in_file[0].split()[1])
    for i in range(1, num_vertices+1):
        line = lines_in_file[i].split()
        line[1] = "\"" + line[1] + "\""
        del line[2:]
        line.append("\n")
        lines_in_file[i] = " ".join(line)
    with open(filename, 'w') as pajek_file:
        for line in lines_in_file:
            pajek_file.write(line)
    print("Written to:", filename)


def write_pajek_for_submodules(json_data, tree_filename="infomap/output/"+"author_graph.tree"):
    """

    :param tree_filename:
    :param json_data:
    :return:
    """
    current_module = 1
    authors_in_module = set()
    with open(tree_filename, 'r') as tree_file:
        for line in tree_file:

            if line[0] == '#':
                continue

            if int(line[:line.index(":")]) > current_module:
                author_graph = nx.DiGraph()
                for msg_id, message in json_data.items():
                    if message['Cc'] is None:
                        addr_list = message['To']
                    else:
                        addr_list = message['To'] | message['Cc']
                    # Adding only the required edges to the authors graph:
                    for to_address in addr_list & authors_in_module:
                        if author_graph.has_edge(message['From'], to_address):
                            author_graph[message['From']][to_address]['weight'] += 1
                        else:
                            author_graph.add_edge(message['From'], to_address, weight=1)
                output_filename = "submodule_"+str(current_module)+".net"
                write_to_pajek(author_graph,filename=output_filename)
                # Run the infomaps algorithm
                output_folder = 'output_submodule' + str(current_module) + "/"
                subprocess.run(args=['mkdir', output_folder])
                subprocess.run(args=['./infomap/Infomap', output_filename + ' ' + output_folder
                               +' --tree --bftree --btree -d -c --node-ranks --flow-network --map'])

                current_module += 1
                authors_in_module = {line[line.index("\"")+1:line.rindex("\"")]}
            else:
                authors_in_module.add(line[line.index("\"")+1:line.rindex("\"")])


def generate_author_communities(json_data):
    """

    :param json_data:
    :return:
    """

    author_graph = igraph.Graph()
    author_graph.es["weight"] = 1.0
    author_map = dict()

    # c_surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1600, 900)
    # ctx = cairo.Context(c_surface)
    # ctx.scale(1900, 900)
    # ctx.rectangle(0, 0, 1, 1)
    # ctx.set_source_rgba(0,0,0,0)
    # ctx.fill()

    """
    Graphs can also be indexed by strings or pairs of vertex indices or vertex names. When a graph is
    indexed by a string, the operation translates to the retrieval, creation, modification or deletion
    of a graph attribute.

    When a graph is indexed by a pair of vertex indices or names, the graph itself is treated as an
    adjacency matrix and the corresponding cell of the matrix is returned. Assigning values different
    from zero or one to the adjacency matrix will be translated to one, unless the graph is weighted,
    in which case the numbers will be treated as weights.
    """
    top_authors = set()
    author_scores = generate_author_ranking(active_score=2, passive_score=1, write_to_file=False)
    index = 0
    for email_addr, author_score in author_scores:
        index += 1
        top_authors.add(email_addr)
        if index == 100:
            break

    index = 0
    for id, node in json_data.items():
        if node['From'] in top_authors:
            if node['From'] not in author_map:
                author_map[node['From']] = index
                author_graph.add_vertex(name=node['From'], label=node['From'])
                index += 1
            for to_addr in node['To']:
                if to_addr in top_authors:
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
                if to_addr in top_authors:
                    if to_addr not in author_map:
                        author_map[to_addr] = index
                        author_graph.add_vertex(name=to_addr, label=to_addr)
                        index += 1
                    if author_graph[node['From'], to_addr] == 0:
                        author_graph.add_edge(node['From'], to_addr, weight=1)
                    else:
                        author_graph[node['From'], to_addr] += 1

    print("Nodes and Edges added to iGraph.")

    # vertex_dendogram = author_graph.community_edge_betweenness(clusters=8, directed=True, weights="weight")
    # igraph.plot(vertex_dendogram, "vd.pdf", vertex_label_size=3, bbox=(1200, 1200))
    # print("Dendrogram saved as PDF.")

    vertex_clustering_obj = author_graph.community_infomap(edge_weights=author_graph.es["weight"])
    igraph.plot(vertex_clustering_obj, "vc.pdf", vertex_label_size=10, bbox=(1500, 1500), edge_color="gray")
    print("Vertex Clustering saved as PDF.")

    # with open("community_vertex_clustering.txt", 'w') as output_file:
    #     output_file.write(str(vertex_clustering_obj))
    #     output_file.close()


def generate_dendrogram_scipy(json_data, tree_filename="infomap/output/"+"author_graph.tree"):
    author_graph = nx.Graph()
    dist_queue = linkage_matrix = pair_queue = list()

    print("Reading author UIDs from JSON file...")
    with open('author_uid_map.json', 'r') as map_file:
        author_uid_map = json.load(map_file)
        map_file.close()

    # Use node_limit to limit the number of authors
    # node_limit = len(author_uid_map)
    node_limit = 50
    buffer_queue = numpy.ndarray((node_limit,2), dtype=float)

    print("Adding nodes to author's graph...")
    for msg_id, message in json_data.items():
        if message['Cc'] is None:
            addr_list = message['To']
        else:
            addr_list = message['To'] | message['Cc']
        for to_address in addr_list:
            if author_graph.has_edge(message['From'], to_address):
                author_graph[message['From']][to_address]['weight'] *= \
                    author_graph[message['From']][to_address]['weight'] / (author_graph[message['From']][to_address]['weight'] + 1)
            else:
                author_graph.add_edge(message['From'], to_address, weight=1)
    shortest_paths = nx.single_source_shortest_path_length(author_graph, 'linux-kernel@vger.kernel.org')

    print("Parsing", tree_filename + "...")
    with open(tree_filename, 'r') as tree_file:
        for line in tree_file:
            if not line or line[0] == '#':
                continue
            line = line.split()
            author_uid = author_uid_map[line[2][1:-1]]
            if author_uid < node_limit:
                if line[2][1:-1] in shortest_paths.keys():
                    buffer_queue[author_uid][0] = shortest_paths[line[2][1:-1]]
                else:
                    buffer_queue[author_uid][0] = 100.0
                buffer_queue[author_uid][1] = float(line[1])
        tree_file.close()

    # for node1 in buffer_queue:
    #     for node2 in buffer_queue:
    #         if node1 != node2 and node1[0] == node2[0]:
    #             node1 = node1[1]
    #             node2 = node2[1]
    #             dist1 = dist2 = float('inf')
    #             if node1 in shortest_paths.keys():
    #                 if node2 in shortest_paths[node1].keys():
    #                     dist1 = shortest_paths[node1][node2]
    #             if node2 in shortest_paths.keys():
    #                 if node1 in shortest_paths[node2].keys():
    #                     dist2 = shortest_paths[node2][node1]
    #             dist_queue.add(min(dist1, dist2), node1, node2)
    # dist_queue.sort(reverse=True)
    #
    # # Using a disjoint set to track the nodes joined:
    # disjoint_set = UnionFind(num_nodes)
    #
    # while dist_queue:
    #     dist1, node1, node2 = dist_queue.pop()
    #     if not disjoint_set.is_connected(node1, node2):
    #         linkage_matrix.add(node1, node2, dist1, 2)
    #         disjoint_set.union(node1, node2)
    #
    # for node1 in buffer_queue:
    #     for node2 in buffer_queue:
    #         if node1 != node2 and node1[0] == node2[0]:
    #             if not disjoint_set.is_connected(node1, node2):
    #                 linkage_matrix.add(node1, node2, dist1, 4)
    #                 disjoint_set.union(node1, node2)

    print("Drawing the dendrogram...")
    linkage_matrix = linkage(buffer_queue, 'single')
    # print(linkage_matrix)

    print("Saving figure to dendrogram_infomaps.png")
    plt.figure(figsize=(80, 40))
    plt.title('Hierarchical Clustering Dendrogram')
    plt.xlabel('Author UID')
    plt.ylabel('Code Length')
    dendrogram(linkage_matrix)
    plt.savefig("dendrogram_infomaps.png")


def generate_dendrogram_plotly(json_data, tree_filename="infomap/output/"+"author_graph.tree"):
    author_graph = nx.Graph()
    dist_queue = linkage_matrix = pair_queue = list()

    print("Reading author UIDs from JSON file...")
    with open('author_uid_map.json', 'r') as map_file:
        author_uid_map = json.load(map_file)
        map_file.close()

    # Use node_limit to limit the number of authors
    # node_limit = len(author_uid_map)
    node_limit = 100

    # buffer_queue = numpy.ndarray((node_limit,2), dtype=float)
    #
    # print("Adding nodes to author's graph...")
    # for msg_id, message in json_data.items():
    #     if message['Cc'] is None:
    #         addr_list = message['To']
    #     else:
    #         addr_list = message['To'] | message['Cc']
    #     for to_address in addr_list:
    #         if author_graph.has_edge(message['From'], to_address):
    #             author_graph[message['From']][to_address]['weight'] *= \
    #                 author_graph[message['From']][to_address]['weight'] / (author_graph[message['From']][to_address]['weight'] + 1)
    #         else:
    #             author_graph.add_edge(message['From'], to_address, weight=1)
    # shortest_paths = nx.single_source_shortest_path_length(author_graph, 'linux-kernel@vger.kernel.org')
    #
    # print("Parsing", tree_filename + "...")
    # with open(tree_filename, 'r') as tree_file:
    #     for line in tree_file:
    #         if not line or line[0] == '#':
    #             continue
    #         line = line.split()
    #         author_uid = author_uid_map[line[2][1:-1]]
    #         if author_uid < node_limit:
    #             if line[2][1:-1] in shortest_paths.keys():
    #                 buffer_queue[author_uid][0] = shortest_paths[line[2][1:-1]]
    #             else:
    #                 buffer_queue[author_uid][0] = 1000.0
    #             buffer_queue[author_uid][1] = float(line[1])
    #     tree_file.close()


    dist_matrix = numpy.ndarray((node_limit, node_limit), dtype=float)

    for msg_id, message in json_data.items():
        if author_uid_map[message['From']] < node_limit:
            if message['Cc'] is None:
                addr_list = message['To']
            else:
                addr_list = message['To'] | message['Cc']
            for to_address in addr_list:
                if author_uid_map[to_address] < node_limit:
                    if author_graph.has_edge(message['From'], to_address):
                        author_graph[message['From']][to_address]['weight'] *= \
                            author_graph[message['From']][to_address]['weight'] / (
                            author_graph[message['From']][to_address]['weight'] + 1)
                    else:
                        author_graph.add_edge(message['From'], to_address, weight=1)
    shortest_paths = nx.all_pairs_shortest_path_length(author_graph)
    print("Nodes added to the author's graph.")

    for i1 in author_graph.nodes():
        for i2 in author_graph.nodes():
            if i2 in shortest_paths[i1]:
                dist_matrix[author_uid_map[i1]][author_uid_map[i2]] = shortest_paths[i1][i2]
            else:
                dist_matrix[author_uid_map[i1]][author_uid_map[i2]] = 100

    print("Drawing the dendrogram...")
    # linkage_matrix = linkage(buffer_queue, 'single')
    # dendro = FF.create_dendrogram(linkage_matrix)

    dendro = FF.create_dendrogram(dist_matrix)
    dendro['layout'].update({'width': 1200, 'height': 800})
    plotly.offline.plot(dendro, filename='dendrogram_infomaps.html')


json_data = dict()
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

write_authors_data_matrix(json_data)