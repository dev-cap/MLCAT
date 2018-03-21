from lib.analysis.author.time_statistics import *
from lib.util.file_util import load_from_disk


def test_inv_func():

    x = 2
    a = 4
    b = 8
    c = 3

    assert inv_func(x, a, b, c) == 7.0


def test_conversation_refresh_times():

    headers_filename1 = './test/integration_test/data/headers_ts.json'
    headers_filename2 = './test/integration_test/data/headers.json'
    graph_nodes = './test/integration_test/data/graph_nodes.csv'
    graph_edges = './test/integration_test/data/graph_edges.csv'
    foldername = './.tmp/integration_test/lib/analysis/author/time_statistics/mailbox'
    req_data1 = './test/integration_test/data/req_data/test_time_statistics1'
    req_data2 = './test/integration_test/data/req_data/test_time_statistics2'

    assert conversation_refresh_times(headers_filename1, graph_nodes, graph_edges, foldername) == None
    assert load_from_disk(foldername+'/conversation_refresh_times.csv') == load_from_disk(req_data1)

    assert conversation_refresh_times(headers_filename1, graph_nodes, graph_edges, foldername, ignore_lat=True) == None
    assert load_from_disk(foldername+'/conversation_refresh_times.csv') == load_from_disk(req_data2)

    assert conversation_refresh_times(headers_filename2, graph_nodes, graph_edges, foldername) == "No messages!"

    # assert conversation_refresh_times(headers_filename, graph_nodes, graph_edges, foldername, plot=True) == None
