from lib.util.union_find import *
import pytest

class TestUnionFind(object):

	def test_find(self):	
		ob=UnionFind(5)
		ob.make_set(5)
		ob.union(4,5)
		assert ob.find(3)==3
		assert ob.find(5)==4
		
	def test_is_connected(self):	
		ob=UnionFind(5)
		ob.make_set(5)
		ob.union(4,2)
		assert ob.is_connected(3,2)==False
		assert ob.is_connected(2,4)==True
		
	def test_parent(self):	
		ob=UnionFind(5)
		ob.make_set(5)
		ob.union(4,2)
		ob.union(3,1)		
		assert ob.parent(2)==4
		assert ob.parent(1)==3
	
