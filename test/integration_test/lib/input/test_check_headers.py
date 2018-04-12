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
		
		obj=CheckHeaders()
		mock_function.return_value.uid.return_value=(1,['5'])
		assert obj.get_unavailable_uid()==set()
	

	@mock.patch('lib.input.check_headers.open_connection')
	def test_check_validity(self,mock_function):

		mock_function.return_value.uid.return_value=(1,['5'])
		obj=CheckHeaders()
		assert obj.check_validity(True, self.headers_file)==5
	

	def test_remove_unwanted_headers(self):

		obj=CheckHeaders()
		obj.check_validity(False,self.headers_file)
		obj.remove_unwanted_headers(obj.unwanted_uid,self.headers_file)
		with open(self.headers_file, 'r') as json_file:
			for chunk in lines_per_n(json_file, 9):
				json_obj = json.loads(chunk)
				assert json_obj['Message-ID'] !=3
	

	def test_remove_duplicate_headers(self):

		obj=CheckHeaders()
		obj.check_validity(False, self.headers_file)
		obj.remove_duplicate_headers(obj.duplicate_uid, self.headers_file)	
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
		obj=CheckHeaders()		
		with open(self.headers_file, 'r') as json_file:
			for chunk in lines_per_n(json_file, 9):
				json_obj = json.loads(chunk)		
		obj.check_validity(False, self.headers_file)
		obj.add_missing_headers(obj.missing_uid,self.unwanted_uid_file,self.uid_map_file)	
		if(obj.missing_uid):
			mock_function.assert_any_call()

	
	@mock.patch('lib.input.imap.header.open_connection')
	def test_replace_invalid_headers(self,mock_function):
		
		mock_function.return_value.uid.return_value=(1,['5'])
		obj=CheckHeaders()
		obj.check_validity(False, self.headers_file)
		obj.replace_invalid_headers(obj.invalid_uid,self.headers_file,self.unwanted_uid_file,self.uid_map_file)
		if(obj.invalid_uid):
			mock_function.assert_any_call()

	
	@mock.patch('lib.input.check_headers.open_connection')
	def test_write_uid_map(self,mock_function):
		
		mock_function.return_value.uid.return_value=(1,['5'])
		obj=CheckHeaders()
		obj.check_validity(False, self.headers_file)
		obj.write_uid_map(1, obj.last_uid_read, self.uid_map_file)
		mock_function.assert_any_call()
