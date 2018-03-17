from lib.util.graph import *


def test_get_current_leaf_nodes():

    list1 = ['1', '2', '3', '4', '5']
    list2 = ['2', '3', '5']
    list3 = ['1', '4']

    assert get_current_leaf_nodes(list1, list2) == list3


def test_get_leaf_nodes():

    list1 = [510, 1108, 1126, 2890, 3272, 3337, 5134, 6150, 6210]

    src_file = './test/integration_test/data/clean_data.json'
    dest_file = './.tmp/integration_test/lib/util/graph/graph_leaf_nodes.csv'

    assert get_leaf_nodes(src_file, dest_file) == list1

    with open(dest_file, 'r') as csv_file:
        csv_content = csv_file.read()
        req_content = "510;511\n1108;1107\n1126;1107\n2890;2891\n3272;3275\n3337;3430\n5134;5139\n6150;6149\n6210;6207\n"
        assert req_content == csv_content
