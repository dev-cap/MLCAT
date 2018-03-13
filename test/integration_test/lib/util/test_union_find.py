from lib.util.union_find import *
import pytest

def test_union_find(self):

	ob=UnionFind(5)
	ob.make_set(5)
	ob.union(1,2)
	ob.union(2,5)
	ob.union(3,4)
	
	assert ob.find(4)==3
	assert ob.find(2)==1
	assert ob.is_connected(3,1)==False
	assert ob.is_connected(2,5)==True
	assert ob.parent(5)==1
	assert ob.parent(4)==3

