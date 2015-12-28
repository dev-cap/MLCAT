from imap_hdr import get_mail_header
from check_headers import *
from data_cleanup import *

last_uid = check_validity()
remove_duplicate_headers()
add_missing_headers()
replace_invalid_headers()

if last_uid == 0:
    last_uid = 1
get_mail_header([last_uid + 1], True)

remove_invalid_references()
