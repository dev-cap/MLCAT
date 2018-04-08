from lib.analysis.author.community import *
from lib.util.file_util import load_from_disk
import unittest
import mock


def test_write_pajek():

    author_graph_file = './test/integration_test/data/author_graph.net'
    author_graph = nx.read_pajek(author_graph_file)

    write_pajek(author_graph, filename=author_graph_file)

    assert nx.is_isomorphic(nx.read_pajek(author_graph_file), author_graph)

@mock.patch("igraph.plot")
def test_vertex_clustering(mock_igraph):

    json_filename = './test/integration_test/data/clean_data.json'
    nodelist_filename = './test/integration_test/data/graph_nodes.csv'
    edgelist_filename = './test/integration_test/data/graph_edges.csv'
    foldername = './.tmp/integration_test/lib/analysis/author/community/vertex_clustering/'
    req_clustering_file = './test/integration_test/data/req_data/test_community1'
    req_list = ['opensuse-kernel@opensuse.org', 'mikky_m@mail.ru', 'gregkh@suse.de', 'doiggl@velocitynet.com.au', 'leyendecker@opensuse.org']

    vertex_clustering(json_filename, nodelist_filename, edgelist_filename, foldername)

    igraph.plot.assert_called()

    assert 'Clustering with 15 elements and 4 clusters' in load_from_disk(foldername+'community_vertex_clustering.txt')

    for email_id in req_list:
        assert email_id in load_from_disk(foldername+'community_vertex_clustering.txt')
