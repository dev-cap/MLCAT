from lib.util.author import *

def test_get_uid_map():

	author_uid_map=dict()
	check='jdelvare@suse.de' in author_uid_map
	assert check==False
	
	author_uid_map=get_uid_map()
	check='jdelvare@suse.de' in author_uid_map
	assert check==True
