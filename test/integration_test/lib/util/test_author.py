from lib.util.author import *
import json

def test_get_uid_map():

	input_data='./test/integration_test/data/clean_data.json'
	test_map='./test/integration_test/data/author_uid_map_test.json'
	expected_map=json.load(open('./test/integration_test/data/author_uid_map.json')).keys()
	
	assert get_uid_map(input_data,test_map).keys()==expected_map
	assert json.load(open(test_map)).keys()==expected_map

