from data_cleanup import remove_invalid_references
from check_headers import *
from graph_edges import generate_edge_list

last_uid = check_validity(False)
print("Last valid UID in JSON file:", last_uid)
remove_duplicate_headers()
# extract_mail_header('lkml.mbox')
remove_invalid_references(True)
generate_edge_list(False)