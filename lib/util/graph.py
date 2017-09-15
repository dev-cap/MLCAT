import json
from util.read import lines_per_n

"""
This module has utility functions for handling graphs and for retriving auxiliary graph properties.
"""

def get_current_leaf_nodes(list1, list2):
    """
    This function eliminates the non-leaf message-ids from the list of leaf message ids.
    
    :param list1: List containing all nodes
    :param list2: Reference list
    :return: List without non-leaf nodes
    """
    s = set(list2)
    list3 = [msg_id for msg_id in list1 if str(msg_id) not in s]
    return list3


def get_leaf_nodes(write_to_file=True):
    """
    This function is used to compute the message-ids of leaf nodes in the thread graph.

    :param write_to_file: If true, writes a list of leaf nodes to graph_leaf_nodes.csv (default = True)
    :return: List of message-ids of leaf nodes
    """
    leaf_msgs = []  # Keeps track of all those message ids that are leaf nodes
    msg_ref_map = {}  # Map between message id of each mail to its references list

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
    return leaf_msgs