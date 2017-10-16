import json
from util.read import lines_per_n


def generate_edge_list(nodelist_filename='graph_nodes.csv', edgelist_filename='graph_edges.csv', json_filename='clean_data.json'):
    """
    This function generates a list of nodes and edges in the graphs from the JSON file and saves it as a CSV file.

    :param nodelist_filename: csv file to store the graph nodes.
    :param edgelist_filename: csv file to store the graph edges.
    :param json_filename: The JSON file containing the cleaned headers.
    """
    # The following set stores all the mail UIDs and the corresponding time as a semi-colon separated string
    nodes = set()
    edges = set()
    with open(json_filename, 'r') as fil:
        for chunk in lines_per_n(fil, 9) :
            jfile = json.loads(chunk)
            msg_id = jfile['Message-ID']
            msg_time = jfile['Time']
            msg_from = "".join(jfile['From'].split())
            nodes.add(str(msg_id) + ";" + msg_from + ";" + msg_time)
            if jfile['References']:
                ref_list = str(jfile['References']).split(',')
                # Message Id of the parent mail is appended to the end of the list of references.
                parent_id = int(ref_list[-1])
                if parent_id and parent_id < msg_id:
                    edges.add((parent_id, msg_id))
            if jfile['In-Reply-To']:
                parent_id = jfile['In-Reply-To']
                if parent_id and parent_id < msg_id:
                    edges.add((parent_id, msg_id))
    with open(nodelist_filename, 'w') as node_file:
        for node_str in nodes:
            node_file.write(node_str + "\n")
    with open(edgelist_filename, 'w') as edge_file:
        for parent_id, msg_id in edges:
            edge_file.write(str(parent_id) + ';' + str(msg_id) + "\n")


def generate_node_labels(nodelist_filename='graph_nodes.txt', edgelist_filename='graph_edges.txt', json_filename='clean_data.json'):
    """

    This function generates a list of nodes and edges in the graphs from the JSON file and saves it as a TXT file.

    :param nodelist_filename: txt file to store the graph nodes.
    :param edgelist_filename: txt file to store the graph edges.
    :param json_filename: The JSON file containing the cleaned headers.
    """
    # The following set stores all the mail UIDs and the corresponding time as a semi-colon separated string
    nodes = set()
    edges = set()
    with open(json_filename, 'r') as fil:
        for chunk in lines_per_n(fil, 9) :
            jfile = json.loads(chunk)
            msg_id = jfile['Message-ID']
            msg_time = jfile['Time']
            msg_from = "".join(jfile['From'].split())
            nodes.add(str(msg_id) + ",")
            if jfile['References']:
                ref_list = str(jfile['References']).split(',')
                # Message Id of the parent mail is appended to the end of the list of references.
                parent_id = int(ref_list[-1])
                if parent_id and parent_id < msg_id:
                    edges.add((parent_id, msg_id))
            if jfile['In-Reply-To']:
                parent_id = jfile['In-Reply-To']
                if parent_id and parent_id < msg_id:
                    edges.add((parent_id, msg_id))
    with open(nodelist_filename, 'w') as node_file:
        for node_str in nodes:
            node_file.write(node_str + "\n")
    with open(edgelist_filename, 'w') as edge_file:
        for parent_id, msg_id in edges:
            edge_file.write(str(parent_id) + '\t' + str(msg_id) + "\n")
