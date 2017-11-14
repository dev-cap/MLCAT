import email
import imaplib
import json

from input.imap.connection import open_connection

from input.imap.header import get_mail_header
from util.read import lines_per_n


def get_unavailable_uid():
	"""

	This function returns a list of UIDs that are not available in the IMAP server.

	:return: List containing the UIDs not available in the IMAP server
	"""
	imaplib._MAXLINE = 800000
	conn = open_connection()
	conn.select('INBOX')
	search_str = 'UID ' + '1:*'
	retcode, uids = conn.uid('SEARCH', None, search_str)

	available_uid = []
	for uid in uids[0].split():
		available_uid.append(int(uid))

	try:
		conn.close()
	except:
		pass
	conn.logout()

	return set(range(min(available_uid), max(available_uid)+1)) - set(available_uid)

# This list stores the UIDs of mails that have duplicate entries in the JSON file.
duplicate_uid = set()

# This set stores the UIDs of mails that don't have an entry in the JSON file - UIDs are consecutive numbers.
missing_uid = set()

# This list stores the UIDs of mails that have entries with insufficient entries in the JSON file.
invalid_uid = set()

# This set stores the UIDs of mails that are not forwarded from LKML subscription which is stored in a text file.
unwanted_uid = set()

# This set stores the UIDs for which corresponding mails are not available in the IMAP server.
unavailable_uid = set()

last_uid_read = 0


def check_validity(check_unavailable_uid='False', json_header_filename='headers.json'):
	"""

	This function checks for and prints duplicate, missing, and invalid objects in the "headers.json" file.
	This function can be run first to generate a list of duplicate, missing, or invalid objects' UIDs which
	can then be used to add or remove their entries from the JSON file.

	:param check_unavailable_uid: If true, prints the unavailable and unwanted uids
	:param json_header_filename: The header file to be parsed
	:return: Last UID that was checked by the function.
	"""
	previous_uid = 0

	# The "read_uid" set is used to keep track of all the UIDs that have been read from the JSON file.
	# In case a duplicate exists, it would be read twice and hence would fail the set membership test.
	read_uid = set([])

	# This variable contains the last UID that was checked. This variable is returned by the function.
	last_valid_uid = 0

	header_attrib = {'Message-ID', 'From', 'To', 'Cc', 'In-Reply-To', 'Time'}

	# Read UIDs of mails that are not forwarded from LKML subscription which is stored in a text file.

	with open(json_header_filename, 'r') as json_file:

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
				duplicate_uid.add(json_obj['Message-ID'])

			# Check if the JSON object has sufficient attributes by checking if "header_attrib" is a subset of its keys
			if not set(header_attrib) <= json_obj.keys() or json_obj['Time'] is None:
				invalid_uid.add(json_obj['Message-ID'])

			# Check if it is a mail that is sent directly to "lkml.subscriber@gmail.com", in which caseit has not been
			# forwarded from the LKML subscription.
			if json_obj['To'] == "lkml.subscriber@gmail.com":
				unwanted_uid.add(json_obj['Message-ID'])

			previous_uid = json_obj['Message-ID']

	# Calculate the missing UIDs by performing a set difference on all the UIDs possible till the highest UID read
	# from the actual UIDs that have been read.
	if previous_uid != 0:
		global last_uid_read
		last_uid_read = max(read_uid)
		global missing_uid
		missing_uid = set(range(min(read_uid), last_uid_read+1)) - read_uid
		global unavailable_uid

	if check_unavailable_uid:
		unavailable_uid = get_unavailable_uid()
		print("Unavailable UIDs: ", unavailable_uid if len(unavailable_uid) > 0 else "None")
		with open("unwanted_uid.txt", 'a') as unw_file:
			for uid in unwanted_uid:
				unw_file.write(str(uid) + '\n')
		print("Unwanted UIDs: ", unwanted_uid if len(unwanted_uid) > 0 else "None")

	print("Duplicate UIDs: ", duplicate_uid if len(duplicate_uid) > 0 else "None")
	print("Missing UIDs: ", missing_uid if len(missing_uid) > 0 else "None")
	print("Invalid UIDs: ", invalid_uid if len(invalid_uid) > 0 else "None")
	return last_uid_read


def remove_unwanted_headers(to_remove=unwanted_uid, json_header_filename='headers.json'):
	"""

	This function removes all the UIDs specified in the to_remove parameter. By default, it removes all the unwanted
	entries in the JSON file, i.e. the list of UIDs of mails that are not forwarded from LKML subscription.

	:param to_remove: A list of UIDs that need to be removed. Default value is the list of unwanted mails' UIDs.
	:param json_header_filename: The header file from which unwanted entries are removed.
	"""
	if len(to_remove) > 0:
		print("Removing unwanted headers...")
		# This list contains a list of JSON objects that need to be written to file
		write_to_file = []

		with open(json_header_filename, 'r') as json_file:
			for chunk in lines_per_n(json_file, 9):
				json_obj = json.loads(chunk)
				if not json_obj['Message-ID'] in unwanted_uid:
					write_to_file.append(json_obj)

		with open(json_header_filename, 'w') as json_file:
			for json_obj in write_to_file:
				json.dump(json_obj, json_file, indent=1)
				json_file.write("\n")


def remove_duplicate_headers(to_remove=duplicate_uid, json_header_filename='headers.json'):
	"""

	This function removes all the duplicate entries of the UIDs specified in the to_remove parameter. By default,
	it removes all the duplicate entries in the JSON file.

	:param to_remove: A list of UIDs that need to be removed. Default value is the list of duplicate mails' UIDs.
	:param json_header_filename: The header file from which duplicate entries are removed.
	"""
	# The "read_uid" set is used to keep track of all the UIDs that have been read from the JSON file.
	# In case a duplicate exists, it would be read twice and hence would fail the set membership test.
	read_uid = set([])

	if len(to_remove) > 0:
		print("Removing duplicate headers...")
		# This list contains a list of JSON objects that need to be written to file
		write_to_file = []

		with open(json_header_filename, 'r') as json_file:
			for chunk in lines_per_n(json_file, 9):
				json_obj = json.loads(chunk)
				if not json_obj['Message-ID'] in read_uid:
					write_to_file.append(json_obj)
				read_uid.add(json_obj['Message-ID'])

		with open(json_header_filename, 'w') as json_file:
			for json_obj in write_to_file:
				json.dump(json_obj, json_file, indent=1)
				json_file.write("\n")


def add_missing_headers(to_add=missing_uid, unwanted_uid_filename="unwanted_uid.txt"):
	"""

	This function adds the mails that have been missed out, considering the fact that UIDs are consecutive.
	If a mail that is missing in the JSON file is not available or has been deleted, this function ignores that UID.

	:param to_add: A list of UIDs that need to be added. Default value is the list of missing mails' UIDs.
	:param unwanted_uid_filename: The file containing unwanted uids
	"""
	# To prevent replacement of mails that are not forwarded from the LKML subscription:
	with open(unwanted_uid_filename, 'r') as unw_file:
		for line in unw_file:
			unwanted_uid.add(int(line.strip()))
	to_add = [x for x in to_add if x not in unwanted_uid]
	# To prevent attempts to replace mails are known to be not available in the IMAP server:
	to_add = [x for x in to_add if x not in unavailable_uid]
	if len(to_add) > 0:
		print("Fetching missing headers...")
		get_mail_header(to_add, False)


def replace_invalid_headers(to_replace=invalid_uid, json_header_filename="headers.json"):
	"""

	This function removes the mail headers that have insufficient attributes and fetches those headers again.
	If an attribute is missing in the original mail header or if the mail has been deleted, this function ignores that UID.

	:param to_replace: A list of UIDs that need to be replaced. Default value is the list of invalid mails' UIDs.
	:param json_header_filename: The json file containing the headers.
	"""
	if len(to_replace) > 0:
		print("Replacing invalid headers...")
		# This list contains a list of JSON objects that need to be written to file
		write_to_file = []
		with open(json_header_filename, 'r') as json_file:
			for chunk in lines_per_n(json_file, 9):
				json_obj = json.loads(chunk)
				if not json_obj['Message-ID'] in invalid_uid:
					write_to_file.append(json_obj)

		with open(json_header_filename, 'w') as json_file:
			for json_obj in write_to_file:
				json.dump(json_obj, json_file, indent=1)
				json_file.write("\n")

		add_missing_headers(to_replace)


def write_uid_map(from_index=1, to_index=last_uid_read, uid_map_filename="thread_uid_map.json"):
	"""
	
	To ensure that references are correctly recorded in the JSON file such that there are no references to mails that
	do not exist and to ease the processing of headers, a map with the string in the Message-Id field of the header to
	the UID of the mail is required. This function fetches the headers from the IMAP server and adds the required
	pairs of Message_ID and UID to the JSON file.
	
	:param from_index: Fetches headers from this UID onwards.
	:param to_index: Fetches headers till this UID (non inclusive).
	:param uid_map_filename: The JSON file where the Message_ID-UID mapping is stored.
	"""
	with open(uid_map_filename, 'r') as map_file:
		uid_msg_id_map = json.load(map_file)
		map_file.close()

	to_get = list(range(from_index, to_index))
	imaplib._MAXLINE = 800000
	conn = open_connection()

	try:
		conn.select('INBOX')

		for num in to_get:
			# conn.uid() converts the arguments provided to an IMAP command to fetch the mail using the UID sepcified by num
			# Uncomment the line below to fetch the entire message rather than just the mail headers.
			# typ, msg_header = conn.uid('FETCH', num, '(RFC822)')
			typ, msg_header = conn.uid('FETCH', str(num), '(RFC822.HEADER)')

			for response_part in msg_header:
				if isinstance(response_part, tuple):
					print("Processing mail #", num)

					# "response_part" contains the required info as a byte stream.
					# This has to be converted to a message stream using the email module
					original = email.message_from_bytes(response_part[1])

					# The splicing is done as to remove the '<' and '>' from the message-id string
					uid_msg_id_map[original['Message-ID'][1:-1]] = num

	finally:
		try:
			conn.close()
		except:
			pass
		conn.logout()

	with open(uid_map_filename, mode='w', encoding='utf-8') as f:
			json.dump(uid_msg_id_map, f, indent=1)
			f.close()
