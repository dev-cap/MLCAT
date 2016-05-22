from data_cleanup import remove_invalid_references
from mbox_hdr import extract_mail_header
from graph_edges import generate_edge_list
from check_headers import *
from util.read_utils import *

extract_mail_header('lkml.mbox')
last_uid = check_validity(False)
print("Last valid UID in JSON file:", last_uid)
remove_duplicate_headers()
remove_invalid_references(True)
generate_edge_list()
get_lone_author_threads(True)