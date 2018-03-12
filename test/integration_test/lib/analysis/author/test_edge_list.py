from lib.analysis.author.edge_list import *
from lib.util.file_util import load_from_disk


def test_generate_edge_list():
    
    author_nodes = './test/integration_test/data/author_nodes.csv'
    author_edges = './test/integration_test/data/author_edges.csv'
    graph_nodes = './test/integration_test/data/graph_nodes.csv'
    graph_edges = './test/integration_test/data/graph_edges.csv'
    clean_data = './test/integration_test/data/clean_data.json'
    author_uid_map = './test/integration_test/data/author_uid_map.json'
    req_data1 = './test/integration_test/data/req_data/test_edge_list1.csv'
    req_data2 = './test/integration_test/data/author_edges.csv'

    generate_edge_list(author_nodes, author_edges, graph_nodes, graph_edges, clean_data, author_uid_map)
    assert nx.is_isomorphic(nx.read_edgelist(author_nodes, delimiter='\t'), nx.read_edgelist(req_data1, delimiter='\t'))
    assert nx.is_isomorphic(nx.read_edgelist(author_edges, delimiter='\t'), nx.read_edgelist(req_data2, delimiter='\t'))

    generate_edge_list(author_nodes, author_edges, graph_nodes, graph_edges, clean_data, author_uid_map, ignore_lat=False)
    assert nx.is_isomorphic(nx.read_edgelist(author_nodes, delimiter='\t'), nx.read_edgelist(req_data1, delimiter='\t'))
    assert nx.is_isomorphic(nx.read_edgelist(author_edges, delimiter='\t'), nx.read_edgelist(req_data2, delimiter='\t'))
    