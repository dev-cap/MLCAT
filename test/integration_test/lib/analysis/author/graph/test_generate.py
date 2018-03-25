from lib.analysis.author.graph.generate import *
import networkx as nx


def test_author_interaction():

    clean_data = './test/integration_test/data/clean_data.json'
    graph_nodes = './test/integration_test/data/graph_nodes.csv'
    graph_edges = './test/integration_test/data/graph_edges.csv'
    pajek_file = './.tmp/integration_test/lib/analysis/author/graph/generate/author_graph.net'
    req_output1 = './test/integration_test/data/req_data/test_generate1.net'
    req_output2 = './test/integration_test/data/req_data/test_generate2.net'

    author_interaction(clean_data, graph_nodes, graph_edges, pajek_file, ignore_lat=True)

    output_graph = nx.read_pajek(pajek_file)
    req_grpah = nx.read_pajek(req_output1)
    assert nx.is_isomorphic(output_graph, req_grpah)

    author_interaction(clean_data, graph_nodes, graph_edges, pajek_file, ignore_lat=False)

    output_graph = nx.read_pajek(pajek_file)
    req_grpah = nx.read_pajek(req_output2)
    assert nx.is_isomorphic(output_graph, req_grpah)
