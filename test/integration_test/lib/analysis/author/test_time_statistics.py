from lib.analysis.author.time_statistics import *
from lib.util.file_util import load_from_disk


def test_inv_func():

    x = 2
    a = 4
    b = 8
    c = 3

    assert inv_func(x, a, b, c) == 7.0


def test_conversation_refresh_times():

    headers_filename = './test/integration_test/data/headers_ts.json'
    graph_nodes = './test/integration_test/data/graph_nodes.csv'
    graph_edges = './test/integration_test/data/graph_edges.csv'
    foldername = './test/integration_test/data/mailbox'
    req_data = './test/integration_test/data/req_data/test_time_statistics'

    assert conversation_refresh_times(headers_filename, graph_nodes, graph_edges, foldername) == None
    assert load_from_disk(foldername+'/conversation_refresh_times.csv') == load_from_disk(req_data)
