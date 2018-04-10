from lib.analysis.author.graph.interaction import *
import unittest
import mock


@mock.patch("networkx.nx_agraph.to_agraph")
@mock.patch("networkx.draw")
def test_weighted_multigraph(mock_nx_to_agraph, mock_nx_draw):
    
    graph_nodes = './test/integration_test/data/graph_nodes_in.csv'
    graph_edges = './test/integration_test/data/graph_edges_in.csv'
    clean_data = './test/integration_test/data/clean_data_in.json'
    output_dir = './.tmp/integration_test/lib/analysis/author/graph/interaction/'
    
    weighted_multigraph(graph_nodes, graph_edges, clean_data, output_dir)
    weighted_multigraph(graph_nodes, graph_edges, clean_data, output_dir, ignore_lat=True)

    mock_nx_draw.assert_called()
