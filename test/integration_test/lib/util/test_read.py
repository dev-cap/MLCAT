from  lib.util.read import *
import json

def test_lines_per_n():	
		
	f = open('./test/integration_test/data/headers.json','r')
	l = lines_per_n(f,9)	
	i = 1
	for j in l:
		jf = json.loads(j)
		assert str(jf['Message-ID']) == str(i)
		i = i+1

def test_get_utc_time():

	kf1=" Wed, 01 Aug 2007 05:23:20 CET "	
	utc_dt1=get_utc_time(kf1)
	assert utc_dt1 == "Wed, 01 Aug 2007 04:23:20 +0000"

def test_get_datetime_object():

	mf=" Wed, 01 Aug 2007 05:23:20 CET "
	utc_dt1=get_datetime_object(mf)
	mf1=datetime.datetime.strptime("Wed, 01 Aug 2007 04:23:20 +0000", "%a, %d %b %Y %H:%M:%S %z")
	mf2 = mf1.astimezone(pytz.utc)
	assert utc_dt1 == mf2

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
