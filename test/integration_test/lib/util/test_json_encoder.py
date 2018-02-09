from lib.util.json_encoder import *
import json

class TestNoIndent(object):

    def test__repr__(self):

        list1 = ["physics", 10, 'a']
        str1 = "physics,10,a"
        noIndentObj = NoIndent(list1)
        assert str(noIndentObj) == str1
        noIndentObj = NoIndent(str1)
        assert str(noIndentObj) == repr(str1)


class TestMyEncoder(object):

    def test_default(self):
        list1 = ["physics", 10, 'a']
        noIndentObj = NoIndent(list1)
        myEncoderObj = MyEncoder()
        assert myEncoderObj.default(noIndentObj) == repr(noIndentObj)
