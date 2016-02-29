import networkx as nx
import json
import re
import csv
from util.read_json import lines_per_n


class MessageNode:
    def __init__(self, msg_id=0, height=-1, parent_id=0, time=None, from_addr=None, to_addr=None, cc_addr=None):
        self.msg_id = msg_id
        self.height = height
        self.parent_id = parent_id
        self.time = time
        self.from_addr = from_addr
        self.to_addr = to_addr
        self.cc_addr = cc_addr

    def __lt__(self,other):
        return (self.height < other.height) if (self.height != other.height) else (self.msg_id < other.msg_id)


def add_thread_nodes(thread_authors, nbunch, parent_id, curr_height):
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
        add_thread_nodes(thread_authors, next_nbunch, node, curr_height + 1)

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
    add_thread_nodes(thread_authors, [origin_node], parent_id=None, curr_height=0)
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
    if origin_node == 5141:
        break