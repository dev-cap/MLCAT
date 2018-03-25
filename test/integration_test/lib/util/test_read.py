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

	kf1=" Wed, 01 Aug 2007 05:23:20 GMT "	
	utc_dt1=get_utc_time(kf1)
	assert utc_dt1 == "Wed, 01 Aug 2007 05:23:20 +0000"
	
	kf2=" Wed, 01 Aug 2007 04:23:20 PST "	
	utc_dt2=get_utc_time(kf2)
	assert utc_dt1 == "Wed, 01 Aug 2007 12:23:20 +0000"
	
	kf3=" Wed, 01 Aug 2007 04:23:20 PDT "	
	utc_dt3=get_utc_time(kf3)
	assert utc_dt1 == "Wed, 01 Aug 2007 12:23:20 +0000"
	
	kf4=" Wed, 01 Aug 2007 04:23:20 EST "	
	utc_dt4=get_utc_time(kf4)
	assert utc_dt1 == "Wed, 01 Aug 2007 09:23:20 +0000"
	
	kf5=" Wed, 01 Aug 2007 05:23:20 EET "	
	utc_dt5=get_utc_time(kf5)
	assert utc_dt1 == "Wed, 01 Aug 2007 03:23:20 +0000"
	
	kf6=" Wed, 01 Aug 2007 05:23:20 CET "	
	utc_dt6=get_utc_time(kf6)
	assert utc_dt1 == "Wed, 01 Aug 2007 04:23:20 +0000"

def test_get_datetime_object():

	mf=" Wed, 01 Aug 2007 05:23:20 CET "
	utc_dt1=get_datetime_object(mf)
	mf1=datetime.datetime.strptime("Wed, 01 Aug 2007 04:23:20 +0000", "%a, %d %b %Y %H:%M:%S %z")
	mf2 = mf1.astimezone(pytz.utc)
	assert utc_dt1 == mf2
	
	mf3=" Wed, 01 Aug 2007 04:23:20 PST "
	utc_dt1=get_datetime_object(mf3)
	mf4=datetime.datetime.strptime("Wed, 01 Aug 2007 12:23:20 +0000", "%a, %d %b %Y %H:%M:%S %z")
	mf5 = mf4.astimezone(pytz.utc)
	assert utc_dt2 == mf5

	mf6=" Wed, 01 Aug 2007 05:23:20 EST "
	utc_dt1=get_datetime_object(mf6)
	mf7=datetime.datetime.strptime("Wed, 01 Aug 2007 10:23:20 +0000", "%a, %d %b %Y %H:%M:%S %z")
	mf8 = mf7.astimezone(pytz.utc)
	assert utc_dt3 == mf8

	mf9=" Wed, 01 Aug 2007 05:23:20 EET "
	utc_dt1=get_datetime_object(mf9)
	mf10=datetime.datetime.strptime("Wed, 01 Aug 2007 03:23:20 +0000", "%a, %d %b %Y %H:%M:%S %z")
	mf11 = mf10.astimezone(pytz.utc)
	assert utc_dt4 == mf11			

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
