import json
from util.read_utils import lines_per_n


def generate_edge_list(ref_toggle=True):
    """
    This function generates a list of nodes and edges in the graphs from the JSON file and saves it as a CSV file.
    :param ref_toggle: If True, References attribute is used to make edges and if False, In-Reply-To is used.
    """
    # The following set stores all the mail UIDs and the corresponding time as a semi-colon separated string
    nodes = set()
    if ref_toggle:
        with open('graph_edges.csv', 'w') as csv_file:
            with open('clean_data.json', 'r') as fil:
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
                        if parent_id:
                            csv_file.write("{0};{1}\n".format(parent_id, msg_id))
                fil.close()
            csv_file.close()
    else:
        with open('graph_edges.csv', 'w') as csv_file:
            with open('clean_data.json', 'r') as fil:
                for chunk in lines_per_n(fil, 9) :
                    jfile = json.loads(chunk)
                    msg_id = jfile['Message-ID']
                    msg_time = jfile['Time']
                    msg_from = "".join(jfile['From'].split())
                    nodes.add(str(msg_id) + ";" + msg_from + ";" + msg_time)
                    if jfile['In-Reply-To']:
                        parent_id = jfile['In-Reply-To']
                        # Message Id of the parent mail is appended to the end of the list of references.
                        if parent_id:
                            csv_file.write("{0};{1}\n".format(parent_id, msg_id))
                fil.close()
            csv_file.close()
    with open('graph_nodes.csv', 'w') as node_file:
        for node_str in nodes:
            node_file.write(node_str + "\n")
