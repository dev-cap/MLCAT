"""
This module is used to  graphs that show the interaction between authors in the mailing list. There is an edge from
one author to another if the former sent a message to the latter either in To or by marking in CC. These graphs are for
the entire mailing list.
"""
import json
import networkx as nx
from util.read import *


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


def write_degree_distribution():
    in_degree_dict = author_graph.in_degree(nbunch=author_graph.nodes_iter())
    out_degree_dict = author_graph.out_degree(nbunch=author_graph.nodes_iter())
    with open("degree_distribution.csv", 'w') as degree_dist_file:
        degree_dist_file.write("Author Email ID,In-Degree,Out-Degree,Degree Differential\n")
        for author_id, out_degree in out_degree_dict.items():
            degree_dist_file.write(author_id + "," + str(in_degree_dict[author_id]) + "," + str(out_degree) + "," + str(out_degree - in_degree_dict[author_id]) + "\n")
        degree_dist_file.close()
    print("Degree distribution written to file.")


def write_clustering_coefficients():
    author_graph_undirected = author_graph.to_undirected()
    clustering_coeff = nx.clustering(author_graph_undirected)
    with open("clustering_coefficients.csv", 'w') as cluster_file:
        cluster_file.write("Author Email ID,Clustering Coeff.\nAverage Clustering,"
                           + str(nx.average_clustering((author_graph_undirected))) + "\n")
        for author_id, coeff in clustering_coeff.items():
            cluster_file.write(author_id + "," + str(coeff) + "\n")
        cluster_file.close()
    print("Clustering coefficients written to file.")


# Time limit can be specified here in the form of a timestamp in one of the identifiable formats. All messages
# that have arrived after time_ubound and before time_lbound will be ignored.
time_ubound = None
time_lbound = None

# If ignore_lat is true, then messages that belong to threads that have only a single author are ignored.
ignore_lat = True

author_graph = nx.DiGraph()
email_re = re.compile(r'[\w\.-]+@[\w\.-]+')
json_data = dict()

if time_ubound is None:
    time_ubound = time.strftime("%a, %d %b %Y %H:%M:%S %z")
time_ubound = get_datetime_object(time_ubound)

if time_lbound is None:
    time_lbound = "Sun, 01 Jan 2001 00:00:00 +0000"
time_lbound = get_datetime_object(time_lbound)

print("All messages before", time_ubound, "and after", time_lbound,  "are being considered.")

if not ignore_lat:
    with open('clean_data.json', 'r') as json_file:
        for chunk in lines_per_n(json_file, 9):
            json_obj = json.loads(chunk)
            json_obj['Message-ID'] = int(json_obj['Message-ID'])
            json_obj['Time'] = datetime.datetime.strptime(json_obj['Time'], "%a, %d %b %Y %H:%M:%S %z")
            if time_lbound <= json_obj['Time'] < time_ubound:
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
                if time_lbound <= json_obj['Time'] < time_ubound:
                    # print("\nFrom", json_obj['From'], "\nTo", json_obj['To'], "\nCc", json_obj['Cc'])
                    from_addr = email_re.search(json_obj['From'])
                    json_obj['From'] = from_addr.group(0) if from_addr is not None else json_obj['From']
                    json_obj['To'] = set(email_re.findall(json_obj['To']))
                    json_obj['Cc'] = set(email_re.findall(json_obj['Cc'])) if json_obj['Cc'] is not None else None
                    # print("\nFrom", json_obj['From'], "\nTo", json_obj['To'], "\nCc", json_obj['Cc'])
                    json_data[json_obj['Message-ID']] = json_obj
    print("JSON data loaded.")

for msg_id, message in json_data.items():
    if message['Cc'] is None:
        addr_list = message['To']
    else:
        addr_list = message['To'] | message['Cc']
    for to_address in addr_list:
        if author_graph.has_edge(message['From'], to_address):
            author_graph[message['From']][to_address]['weight'] += 1
        else:
            author_graph.add_edge(message['From'], to_address, weight=1)

print("Authors graph generated with nodes:", nx.number_of_nodes(author_graph), end=" ")
print("and edges:", nx.number_of_edges(author_graph))
write_to_pajek(author_graph)
write_degree_distribution()
write_clustering_coefficients()
