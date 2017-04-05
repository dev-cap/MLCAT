"""
This module is used to  graphs that show the interaction between authors in the mailing list. There is an edge from
one author to another if the former sent a message to the latter either in To or by marking in CC. These graphs are for
the entire mailing list.
"""
import json
from util.read_utils import *


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

# Time limit can be specified here in the form of a timestamp in one of the identifiable formats and all messages
# that have arrived after this timestamp will be ignored.
time_limit = None
# If true, then messages that belong to threads that have only a single author are ignored.
ignore_lat = True
author_graph = nx.DiGraph()
email_re = re.compile(r'[\w\.-]+@[\w\.-]+')
json_data = dict()
if time_limit is None:
    time_limit = time.strftime("%a, %d %b %Y %H:%M:%S %z")
msgs_before_time = set()
time_limit = get_datetime_object(time_limit)
print("All messages before", time_limit, "are being considered.")

time_lbound = "Sun, 01 Jan 2001 00:00:00 +0000"
time_lbound = get_datetime_object(time_lbound)
time_ubound=time_limit
print("All messages before", time_ubound, "and after", time_lbound, "are being considered.")

#call the method from read_utils
load_json(ignore_lat, time_lbound, time_ubound, email_re, json_data, json_filename="clean_data.json")

for msg_id, message in json_data.items():
    if message['Cc'] is None:
        addr_list = message['To']
    else:
        addr_list = message['To'] | message['Cc']
    for to_address in addr_list:
        author_graph.add_edge(message['From'], to_address)

write_to_pajek(author_graph)

print("No. of Weakly Connected Components:", nx.number_weakly_connected_components(author_graph))
print("No. of Strongly Connected Components:", nx.number_strongly_connected_components(author_graph))
print("Nodes:", nx.number_of_nodes(author_graph))
print("Edges:", nx.number_of_edges(author_graph))
