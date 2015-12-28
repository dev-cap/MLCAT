from itertools import islice, chain
from imap_hdr import get_mail_header
import json


def lines_per_n(f, n):
    """
    Each json object in the headers.json file occupies a set number of lines.
    This function is used to read those set number of lines and return them.
    """
    for line in f :
        yield ''.join(chain([line], islice(f, n-1)))

# This list stores the list of UIDs of mails that have duplicate entries in the JSON file.
duplicate_uid = []

# This list stores the list of UIDs of mails that don't have an entry in the JSON file - UIDs are consecutive numbers.
missing_uid = []

# This list stores the list of UIDs of mails that have entries with insufficient entries in the JSON file.
invalid_uid = []


def check_validity():
    """
    This function checks for and prints duplicate, missing, and invalid objects in the "headers.json" file.
    This function can be run first to generate a list of duplicate, missing, or invalid objects' UIDs which
    can then be used to add or remove their entries from the JSON file.
    :return: Last UID that was checked by the function.
    """

    previous_uid = 0;

    # The "read_uid" set is used to keep track of all the UIDs that have been read from the JSON file.
    # In case a duplicate exists, it would be read twice and hence would fail the set membership test.
    read_uid = set([])

    # This variable contains the last UID that was checked. This variable is returned by the function.
    last_valid_uid = 0

    header_attrib = {'Message-ID', 'From', 'To', 'Cc', 'In-Reply-To', 'Time'}

    with open('headers.json', 'r') as json_file:

        for chunk in lines_per_n(json_file, 9):
            try:
                json_obj = json.loads(chunk)
            except:
                print("Unreadable JSON object after UID: " + str(previous_uid))
                break

            # Checking for duplicate objects
            if not json_obj['Message-ID'] in read_uid:
                read_uid.add(json_obj['Message-ID'])
            else:
                duplicate_uid.append(json_obj['Message-ID'])

            # Check if the JSON object has sufficient attributes by checking if "header_attrib" is a subset of its keys
            if not set(header_attrib) <= json_obj.keys() or json_obj['Time'] is None:
                invalid_uid.append(json_obj['Message-ID'])

            previous_uid = json_obj['Message-ID']

    # Calculate the missing UIDs by performing a set difference on all the UIDs possible till the highest UID read
    # from the actual UIDs that have been read.
    if previous_uid != 0:
        global missing_uid
        missing_uid += list(set(range(min(read_uid), max(read_uid)+1)) - read_uid)

    print("Duplicate UIDs: ", duplicate_uid)
    print("Missing UIDs: ", missing_uid)
    print("Invalid UIDs: ", invalid_uid)
    return previous_uid


def remove_duplicate_headers(to_remove=duplicate_uid):
    """
    This function removes all the UIDs specified in the to_remove parameter. By default, it removes all the duplicate
    entries in the JSON file.
    :param to_remove: A list of UIDs that need to be removed. Default value is the list of duplicate mails' UIDs.
    """
    # The "read_uid" set is used to keep track of all the UIDs that have been read from the JSON file.
    # In case a duplicate exists, it would be read twice and hence would fail the set membership test.
    read_uid = set([])

    if len(to_remove) > 0:

        # This list contains a list of JSON objects that need to be written to file
        write_to_file = []

        with open('headers.json', 'r') as json_file:
            for chunk in lines_per_n(json_file, 9):
                json_obj = json.loads(chunk)
                if not json_obj['Message-ID'] in read_uid:
                    write_to_file.append(json_obj)
                read_uid.add(json_obj['Message-ID'])

        with open('headers.json', 'w') as json_file:
            for json_obj in write_to_file:
                json.dump(json_obj, json_file, indent=1)
                json_file.write("\n")


def add_missing_headers(to_add=missing_uid):
    """
    This function adds the mails that have been missed out, considering the fact that UIDs are consecutive.
    If a mail that is missing in the JSON file is not available or has been deleted, this function ignores that UID.
    :param to_add: A list of UIDs that need to be added. Default value is the list of missing mails' UIDs.
    """
    if len(to_add) > 0:
        get_mail_header(to_add, False)


def replace_invalid_headers(to_replace=invalid_uid):
    """
    This function removes the mail headers that have insufficient attributes and fetches those headers again.
    If an attribute is missing in the original mail header or if the mail has been deleted, this function ignores that UID.
    :param to_replace: A list of UIDs that need to be replaced. Default value is the list of invalid mails' UIDs.
    """
    if len(to_replace) > 0:
        # This list contains a list of JSON objects that need to be written to file
        write_to_file = []
        with open('headers.json', 'r') as json_file:
            for chunk in lines_per_n(json_file, 9):
                json_obj = json.loads(chunk)
                if not json_obj['Message-ID'] in invalid_uid:
                    write_to_file.append(json_obj)

        with open('headers.json', 'w') as json_file:
            for json_obj in write_to_file:
                json.dump(json_obj, json_file, indent=1)
                json_file.write("\n")

        add_missing_headers(to_replace)
