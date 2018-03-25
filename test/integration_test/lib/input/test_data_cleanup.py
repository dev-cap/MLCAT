from lib.input.data_cleanup import *
from lib.util.read import lines_per_n
import json


def test_remove_invalid_references():

    input_json_filename = './test/integration_test/data/headers_for_cleanup.json'
    output_json_filename = './.tmp/integration_test/lib/input/data_cleanup/clean_headers.json'

    remove_invalid_references(input_json_filename, output_json_filename, ref_toggle=True)

    with open(output_json_filename, 'r') as clean_headers:
        for chunk in lines_per_n(clean_headers, 9):
            jfile = json.loads(chunk)
            assert jfile['Message-ID'] == 500 or 510
