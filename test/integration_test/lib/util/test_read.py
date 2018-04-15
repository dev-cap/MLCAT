from  lib.util.read import *
import json

def test_lines_per_n():	
		
	f = open('./test/integration_test/data/headers.json','r')
	l = lines_per_n(f,9)	
	i = 1
	for j in l:
		jf = json.loads(j)
		assert str(jf['Message-ID']) == str(i)
		if i == 2:
			i = 9
		else: 
			i = i+1	
		

def test_get_utc_time():

	date1 = " Wed, 01 Aug 2007 05:23:20 GMT "	
	date2 = " Wed, 01 Aug 2007 05:23:20 PST "
	date3 = " Wed, 01 Aug 2007 05:23:20 PDT "
	date4 = " Wed, 01 Aug 2007 05:23:20 EST "
	date5 = " Wed, 01 Aug 2007 05:23:20 EET "
	date6 = " Wed, 01 Aug 2007 05:23:20 CET "

	utc_dt1 = get_utc_time(date1)
	utc_dt2 = get_utc_time(date2)
	utc_dt3 = get_utc_time(date3)
	utc_dt4 = get_utc_time(date4)
	utc_dt5 = get_utc_time(date5)
	utc_dt6 = get_utc_time(date6)
	
	assert utc_dt1 == "Wed, 01 Aug 2007 05:23:20 +0000"
	assert utc_dt2 == "Wed, 01 Aug 2007 13:23:20 +0000"
	assert utc_dt3 == "Wed, 01 Aug 2007 13:23:20 +0000"
	assert utc_dt4 == "Wed, 01 Aug 2007 10:23:20 +0000"
	assert utc_dt5 == "Wed, 01 Aug 2007 03:23:20 +0000"
	assert utc_dt6 == "Wed, 01 Aug 2007 04:23:20 +0000"


def test_get_datetime_object():

	date1 = "  01 Aug 2007 05:23:20 GMT "	
	date2 = " Wed, 01 Aug 2007 05:23:20 PST "
	date3 = " Wed, 01 Aug 2007 05:23:20 EST "
	date4 = " Wed, 01 Aug 2007 05:23:20 EET "
	date5 = " Wed, 01 Aug 2007 05:23:20 CET "

	utc_dt1 = get_datetime_object(date1)
	utc_dt2 = get_datetime_object(date2)
	utc_dt3 = get_datetime_object(date3)
	utc_dt4 = get_datetime_object(date4)
	utc_dt5 = get_datetime_object(date5)
	
	assert str(utc_dt1) == "2007-08-01 05:23:20+00:00"
	assert str(utc_dt2) == "2007-08-01 13:23:20+00:00"
	assert str(utc_dt3) == "2007-08-01 10:23:20+00:00"
	assert str(utc_dt4) == "2007-08-01 03:23:20+00:00"
	assert str(utc_dt5) == "2007-08-01 04:23:20+00:00"


def test_get_messages_before():
	
	nf=" Tue, 23 Dec 2014 10:17:57 GMT "
	file_name='./test/integration_test/data/graph_nodes_read.csv'
	n=get_messages_before(nf,file_name)
	n1={43639,11622,37690,18081,50823,24533,176,38086,40158,51348}
	assert n == n1


def test_get_lone_author_threads():
    
    graph_nodes = './test/integration_test/data/graph_nodes_read.csv'
    graph_edges = './test/integration_test/data/graph_edges_read.csv'

    output = get_lone_author_threads(nodelist_filename=graph_nodes, edgelist_filename=graph_edges)

    req_output = {18081, 11622, 50823, 38086, 176, 51348, 24533, 43639, 37690, 40158}
    
    assert req_output == output	
