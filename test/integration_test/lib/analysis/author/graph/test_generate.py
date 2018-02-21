from lib.analysis.author.graph.generate import *


def test_author_interaction():

    clean_data = './test/integration_test/data/clean_data.json'
    graph_nodes = './test/integration_test/data/graph_nodes.csv'
    graph_edges = './test/integration_test/data/graph_edges.csv'
    pajek_file = './test/integration_test/data/author_graph.net'
    req_output1 = './test/integration_test/data/req_data/test_generate1'
    req_output2 = './test/integration_test/data/req_data/test_generate2'

    author_interaction(clean_data, graph_nodes, graph_edges, pajek_file, ignore_lat=True)

    with open(req_output1, 'r') as req_output_file:
        with open(pajek_file, 'r') as output_file:
            assert output_file.readlines()[0] == req_output_file.readlines()[0]

    author_interaction(clean_data, graph_nodes, graph_edges, pajek_file, ignore_lat=False)

    with open(req_output2, 'r') as req_output_file:
        with open(pajek_file, 'r') as output_file:
            assert output_file.readlines()[0] == req_output_file.readlines()[0]
