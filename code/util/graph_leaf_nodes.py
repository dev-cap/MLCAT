from itertools import islice, chain
import json

leaf_msgs = []  # Keeps track of all those message ids that are leaf nodes
msg_ref_map = {}  # Map between message id of each mail to its references list


# Function to read a json object from the file
def lines_per_n(f, n):
    for line in f:
        yield ''.join(chain([line], islice(f, n - 1)))


# Function to eliminate the non-leaf message-ids from the list of leaf message ids.
def get_current_leaf_nodes(list1, list2):
    s = set(list2)
    list3 = [msg_id for msg_id in list1 if str(msg_id) not in s]
    return list3

"""
For each json object read, we add the message id into the list leaf_msgs and create an entry of the particular id in the map
msg_ref_map. We then check if any non-leaf message ids are present in the list leaf_msgs by calling the function get_current_leaf_nodes.
After going through the entire file, we then print the leaf message-ids and their references. This is stored in the file thread_paths.txt
"""
with open('clean_data.json', 'r') as fil:
    for chunk in lines_per_n(fil, 9):

        jfile = json.loads(chunk)

        leaf_msgs.append(jfile['Message-ID'])
        msg_ref_map[jfile['Message-ID']] = str(jfile['References'])

        if not (jfile['References'] == None):
            leaf_msgs = get_current_leaf_nodes(leaf_msgs, jfile['References'].split(','))

    fil.close()

with open('graph_leaf_nodes.csv', 'w') as csv_file:
    for msg_id in leaf_msgs:
        csv_file.write("{0};{1}\n".format(msg_id, msg_ref_map[msg_id]))
    csv_file.close()