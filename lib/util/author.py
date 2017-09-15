import json
import re
from util.read import lines_per_n


def get_uid_map(write_to_file=True):
    """

    This function is used to generate and write to a JSON file the mapping of authors to a unique integer identifier.
    Authors are identified through a regular expression search for their email addresses. The integer identifiers
    generated are used in other modules like the generation and statistical analysis of hyperedges.
    
    :param write_to_file: If true, results are written to author_uid_map.json (default=True)
    :return: A list of all message ids that are leaf nodes
    """
    index = 0
    author_set = set()
    author_uid_map = dict()
    email_re = re.compile(r'[\w\.-]+@[\w\.-]+')

    with open('clean_data.json', 'r') as json_file:
        for chunk in lines_per_n(json_file, 9):
            json_obj = json.loads(chunk)
            from_addr = email_re.search(json_obj['From'])
            author_set.add(from_addr.group(0) if from_addr is not None else json_obj['From'])
            author_set |= set(email_re.findall(json_obj['To']))
            if json_obj['Cc'] is not None:
                author_set |= set(email_re.findall(json_obj['Cc']))
    print("JSON data loaded.")

    for address in author_set:
        author_uid_map[address] = index
        index += 1

    with open("author_uid_map.json", 'w') as map_file:
        json.dump(author_uid_map, map_file, indent=1)
        map_file.close()
    print("UID map written to author_uid_map.json.")
    return author_uid_map
