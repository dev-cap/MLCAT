from lib.analysis.author.ranking import * 
from lib.util.file_util import *


def test_get():

    json_filename = './test/integration_test/data/headers.json'
    output_filename = './test/integration_test/data/author_ranking.csv'
    req_ranking = [('opensuse-kernel@opensuse.org', 5), ('aiaredir@yahoo.com', 4), ('jeffm@suse.com', 3), ('aj@suse.de', 2)]
    req_csv = './test/integration_test/data/req_data/test_ranking'
    assert list(get(json_filename, output_filename, active_score=2, passive_score=1)) == req_ranking
    print(get(json_filename, output_filename, active_score=2, passive_score=1))
    with open(output_filename, 'r') as rank_file:
        rank_data = rank_file.read()
        assert rank_data == load_from_disk(req_csv)

