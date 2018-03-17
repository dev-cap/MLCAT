from lib.analysis.author.wh_table import *
from lib.util.file_util import *


def test_generate_wh_table_authors():

    nodelist_filename = './test/integration_test/data/graph_nodes.csv'
    edgelist_filename = './test/integration_test/data/graph_edges.csv'
    output_filename = './.tmp/integration_test/lib/analysis/author/wh_table/wh_table_authors.csv'

    req_file_data1 = './test/integration_test/data/req_data/test_wh_table1'
    req_file_data2 = './test/integration_test/data/req_data/test_wh_table2'

    generate_wh_table_authors(nodelist_filename, edgelist_filename, output_filename)

    with open(output_filename, 'r') as wh_table_file:
        wh_table_data = wh_table_file.read()
        assert wh_table_data == load_from_disk(req_file_data1)

    generate_wh_table_authors(nodelist_filename, edgelist_filename, output_filename, ignore_lat=True)

    with open(output_filename, 'r') as wh_table_file:
        wh_table_data = wh_table_file.read()
        assert wh_table_data == load_from_disk(req_file_data2)
