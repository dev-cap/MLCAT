import json
from util.read_json import lines_per_n
import community
import networkx as nx

author_graph = nx.DiGraph()
with open('clean_data.json', 'r') as jfile:
    for chunk in lines_per_n(jfile, 9):
        hdr_data = json.loads(chunk)
        for to_addr in str(hdr_data['To']).split(","):
            if '@' in to_addr:
                author_graph.add_edge(str(hdr_data['From']), to_addr.strip(), style='solid', label=hdr_data['Time'])
        for cc_addr in str(hdr_data['Cc']).split(","):
            if '@' in to_addr:
                author_graph.add_edge(str(hdr_data['From']), cc_addr.strip(), style='dashed', label=hdr_data['Time'])
    jfile.close()

print("No. of Weakly Connected Components:", nx.number_weakly_connected_components(author_graph))
print("No. of Strongly Connected Components:", nx.number_strongly_connected_components(author_graph))
print("Nodes:", nx.number_of_nodes(author_graph))
print("Edges:", nx.number_of_edges(author_graph))

#The following lines of code generate a dendogram for the above graph
dendo = community.generate_dendogram(author_graph.to_undirected())
for level in range(len(dendo)) :
    print("Partition at level", level, "is", community.partition_at_level(dendo, level))
    print("-"*10)
