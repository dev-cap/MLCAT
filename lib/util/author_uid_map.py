import json
import re
from util.read_json import lines_per_n


def write_author_uid_map():

    index = 0
    author_set = set()
    author_uid_map = dict()
    email_re = re.compile(r'[\w\.-]+@[\w\.-]+')

    with open('clean_data.json', 'r') as json_file:
        for chunk in lines_per_n(json_file, 9):
            json_obj = json.loads(chunk)
            # print("\nFrom", json_obj['From'], "\nTo", json_obj['To'], "\nCc", json_obj['Cc'])
            from_addr = email_re.search(json_obj['From'])
            author_set.add(from_addr.group(0) if from_addr is not None else json_obj['From'])
            author_set |= set(email_re.findall(json_obj['To']))
            if json_obj['Cc'] is not None:
                author_set |= set(email_re.findall(json_obj['Cc']))
            # print("\nFrom", json_obj['From'], "\nTo", json_obj['To'], "\nCc", json_obj['Cc'])
    print("JSON data loaded.")

    for address in author_set:
        author_uid_map[address] = index
        index += 1

    with open("author_uid_map.json", 'w') as map_file:
        json.dump(author_uid_map, map_file, indent=1)
        map_file.close()
    print("UID map written to author_uid_map.json.")
write_author_uid_map()