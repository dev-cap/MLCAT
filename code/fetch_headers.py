from check_headers import *
from data_cleanup import *

# Uncomment the following line to update "uid_map.json"
# write_uid_map(1, 57635)

last_uid = check_validity()
remove_duplicate_headers()
remove_unwanted_headers()
add_missing_headers()
replace_invalid_headers()

get_mail_header([last_uid+1], True)
remove_invalid_references()
