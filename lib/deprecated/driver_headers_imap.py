from lib.analysis.thread import generate_edge_list
from lib.input.check_headers import *
from lib.input.data_cleanup import *

# Uncomment the following line to update "uid_map.json"
# write_uid_map(1, 57635)

obj=CheckHeaders()
last_uid = obj.check_validity(True)
obj.remove_duplicate_headers()
obj.remove_unwanted_headers()
obj.add_missing_headers()
obj.replace_invalid_headers()

get_mail_header([last_uid+1], True)
remove_invalid_references()
generate_edge_list(True)
