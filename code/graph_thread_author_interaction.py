import json
import re
import networkx as nx
from util.json_utils import lines_per_n


def add_to_multigraph(graph_obj, discussion_graph, json_data, nbunch, label_prefix=''):
    i = 0
    for node in sorted(nbunch):
        node_attr = json_data[node]
        if node_attr['Cc'] is None:
            addr_list = node_attr['To']
        else:
            addr_list = node_attr['To'] | node_attr['Cc']
        for to_address in addr_list:
            graph_obj.add_edge(node_attr['From'], to_address, label=label_prefix+str(i))
        succ_nbunch = [int(x) for x in discussion_graph.successors(str(node))]
        if succ_nbunch is not None:
            add_to_multigraph(graph_obj, discussion_graph, json_data, succ_nbunch, label_prefix+str(i)+'.')
        i += 1


def author_interaction_multigraph(discussion_graph, json_data, limit=10):
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
        succ_nbunch = [int(x) for x in discussion_graph.successors(str(node))]
        if succ_nbunch is not None:
            add_to_weighted_graph(graph_obj, discussion_graph, json_data, succ_nbunch, node_enum)


def author_interaction_weighted_graph(discussion_graph, json_data, limit=10):
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

with open('headers.json', 'r') as json_file:
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

