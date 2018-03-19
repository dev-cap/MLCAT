from lib.util.union_find import *
import pytest

class TestUnionFind(object):

	def test_make_set(self):	
		with pytest.raises(TypeError):
			ob=UnionFind('a')
		with pytest.raises(ValueError):
			ob=UnionFind(-1)
			
		ob=UnionFind(5)
		ob.make_set(5)
		with pytest.raises(TypeError):
			ob.make_set('a')
		with pytest.raises(ValueError):
			ob.make_set(-1)
		
	def test_union(self):	
		ob=UnionFind(5)
		ob.union(4,2)
		with pytest.raises(TypeError):
			ob.union(1,'a')
		with pytest.raises(ValueError):
			ob.union(1,-1)
	
	def test_find(self):					
		ob=UnionFind(5)
		ob.union(4,2)
		assert ob.find(3)==3
		assert ob.find(2)==4	
	
	def test_is_connected(self):
		ob=UnionFind(5)
		ob.union(4,2)
		assert ob.is_connected(3,2)==False
		assert ob.is_connected(2,4)==True
		
	def test_parent(self):	
		ob=UnionFind(5)
		ob.union(4,2)			
		assert ob.parent(1)==1
		assert ob.parent(2)==4
	
