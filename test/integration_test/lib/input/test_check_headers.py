import unittest 
import mock
from lib.input.check_headers import *

headers_file='./test/integration_test/data/headers_for_check.json'
unwanted_uid_file='./test/integration_test/data/unwanted_uid.txt'
uid_map_file='./test/integration_test/data/thread_uid_map.json'

@mock.patch('lib.input.check_headers.open_connection')
def test_get_unavailable_uid(mock_function):

	mock_function.return_value.uid.return_value=(1,['5'])
	assert get_unavailable_uid()==set()
	
def test_check_validity():

	assert check_validity(False, headers_file)==5
	
def test_remove_unwanted_headers():

	check_validity(False,headers_file)
	remove_unwanted_headers(unwanted_uid,headers_file)
	with open(headers_file, 'r') as json_file:
		for chunk in lines_per_n(json_file, 9):
			json_obj = json.loads(chunk)
			assert json_obj['Message-ID'] !=3
	
def test_remove_duplicate_headers():

	check_validity(False, headers_file)
	remove_duplicate_headers(duplicate_uid,headers_file)	
	count_uid=0
	with open(headers_file, 'r') as json_file:
		for chunk in lines_per_n(json_file, 9):
			json_obj = json.loads(chunk)
			if json_obj['Message-ID'] ==2:
				count_uid=count_uid+1
	assert count_uid==1

@mock.patch('lib.input.imap.header.open_connection')
def test_add_missing_headers(mock_function):

	mock_function.return_value.uid.return_value=(1,['5'])
	with open(headers_file, 'r') as json_file:
		for chunk in lines_per_n(json_file, 9):
			json_obj = json.loads(chunk)
	check_validity(False, headers_file)
	add_missing_headers(missing_uid,unwanted_uid_file,uid_map_file)	
	if(missing_uid):
		mock_function.assert_any_call()

@mock.patch('lib.input.imap.header.open_connection')
def test_replace_invalid_headers(mock_function):
	mock_function.return_value.uid.return_value=(1,['5'])
	check_validity(False, headers_file)
	replace_invalid_headers(invalid_uid,headers_file,unwanted_uid_file,uid_map_file)
	if(invalid_uid):
		mock_function.assert_any_call()

@mock.patch('lib.input.check_headers.open_connection')
def test_write_uid_map(mock_function):
	mock_function.return_value.uid.return_value=(1,['5'])
	check_validity(False, headers_file)
	write_uid_map(1,last_uid_read,uid_map_file)
	mock_function.assert_any_call()
	
