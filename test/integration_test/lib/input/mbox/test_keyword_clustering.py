from lib.input.mbox.keyword_clustering import *
import numpy as np


def test_get_top_authors():

    top_n = 3
    json_filename = './test/integration_test/data/headers.json'
    req_set = ({'opensuse-kernel@opensuse.org', 'jeffm@suse.com', 'aiaredir@yahoo.com'}, {'opensuse-kernel@opensuse.org': 1, 'aiaredir@yahoo.com': 2, 'jeffm@suse.com': 3})
    assert get_top_authors(top_n, json_filename) == req_set
