from itertools import islice, chain
import json


def lines_per_n(f, n) :

    for line in f :
        yield ''.join(chain([line], islice(f, n-1)))

# The following set stores all the mail UIDs and the corresponding time as a semi-colon separated string
nodes = set()

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
                csv_file.write("{0};{1}\n".format(parent_id, msg_id))
        fil.close()
    csv_file.close()

with open('graph_nodes.csv', 'w') as node_file:
    for node_str in nodes:
        node_file.write(node_str + "\n")