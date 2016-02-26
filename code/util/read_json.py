from itertools import islice, chain

def lines_per_n(f, n):
    """
    Each json object in the headers.json file occupies a set number of lines.
    This function is used to read those set number of lines and return them.
    """
    for line in f :
        yield ''.join(chain([line], islice(f, n-1)))
