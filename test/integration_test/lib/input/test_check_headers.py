import unittest 
import mock
import json
from lib.util.read import lines_per_n
from lib.input.check_headers import CheckHeaders


class TestCheckHeaders(object):	
	
	headers_file='./test/integration_test/data/headers_for_check.json'
	unwanted_uid_file='./test/integration_test/data/unwanted_uid.txt'
	uid_map_file='./test/integration_test/data/thread_uid_map.json'


	@mock.patch('lib.input.check_headers.open_connection')
	def test_get_unavailable_uid(self,mock_function):
		
		checkHeaders=CheckHeaders()
		mock_function.return_value.uid.return_value=(1,['5'])
		assert checkHeaders.get_unavailable_uid()==set()
	

	@mock.patch('lib.input.check_headers.open_connection')
	def test_check_validity(self,mock_function):

		mock_function.return_value.uid.return_value=(1,['5'])
		checkHeaders=CheckHeaders()
		assert checkHeaders.check_validity(True, self.headers_file)==5
	

	def test_remove_unwanted_headers(self):

		checkHeaders=CheckHeaders()
		checkHeaders.check_validity(False,self.headers_file)
		checkHeaders.remove_unwanted_headers(checkHeaders.unwanted_uid,self.headers_file)
		with open(self.headers_file, 'r') as json_file:
			for chunk in lines_per_n(json_file, 9):
				json_obj = json.loads(chunk)
				assert json_obj['Message-ID'] !=3
	

	def test_remove_duplicate_headers(self):

		checkHeaders=CheckHeaders()
		checkHeaders.check_validity(False, self.headers_file)
		checkHeaders.remove_duplicate_headers(checkHeaders.duplicate_uid, self.headers_file)	
		count_uid=0
		with open(self.headers_file, 'r') as json_file:
			for chunk in lines_per_n(json_file, 9):
				json_obj = json.loads(chunk)
				if json_obj['Message-ID'] ==2:
					count_uid=count_uid+1
		assert count_uid==1


	@mock.patch('lib.input.imap.header.open_connection')
	def test_add_missing_headers(self,mock_function):

		mock_function.return_value.uid.return_value=(1,['5'])
		checkHeaders=CheckHeaders()		
		with open(self.headers_file, 'r') as json_file:
			for chunk in lines_per_n(json_file, 9):
				json_obj = json.loads(chunk)		
		checkHeaders.check_validity(False, self.headers_file)
		checkHeaders.add_missing_headers(checkHeaders.missing_uid,self.unwanted_uid_file,self.uid_map_file)	
		if(checkHeaders.missing_uid):
			mock_function.assert_any_call()

	
	@mock.patch('lib.input.imap.header.open_connection')
	def test_replace_invalid_headers(self,mock_function):
		
		mock_function.return_value.uid.return_value=(1,['5'])
		checkHeaders=CheckHeaders()
		checkHeaders.check_validity(False, self.headers_file)
		checkHeaders.replace_invalid_headers(checkHeaders.invalid_uid,self.headers_file,self.unwanted_uid_file,self.uid_map_file)
		if(checkHeaders.invalid_uid):
			mock_function.assert_any_call()

	
	@mock.patch('lib.input.check_headers.open_connection')
	def test_write_uid_map(self,mock_function):
		
		mock_function.return_value.uid.return_value=(1,['5'])
		checkHeaders=CheckHeaders()
		checkHeaders.check_validity(False, self.headers_file)
		checkHeaders.write_uid_map(1, checkHeaders.last_uid_read, self.uid_map_file)
		mock_function.assert_any_call()
