"""
This class is used for pretty printing in a json file. Normal json behaviour is to print all the elements of a list
on separate lines. Here we convert a list into a string of comma separated elements of the list. This helps containing
the elements of the list in a single line.
"""
import json

class NoIndent(object):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        """
        This function converts the elements of the list into strings and perform a join on them to a comma-separated string containing all the elements.
        """
        if not isinstance(self.value, list):
            return repr(self.value)
        else:
            string_list = []
            for x in self.value:
                string_list.append(str(x))

            return ','.join(string_list)


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        """
        For objects of the NoIndent class, custom separation is used. Otherwise the default represenation provided by JSON.
        """
        return (repr(obj) if isinstance(obj, NoIndent) else
                json.JSONEncoder.default(self, obj))
