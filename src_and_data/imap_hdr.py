import imaplib
import pprint
import email
import json
from encoder import NoIndent, MyEncoder
from imap_conn import open_connection

"""
This is used to map the string in the Message-Id field of the header to the UID of the mail.
By doing so we ease the further processing of information.
"""
uid_msg_id_map = {}

"""
The issue lies in with the fact that we are trying to download a whole list of messages in the inbox at once.
This causes a buffer overflow and hence imaplib raises an error(the max it allows, by default, is 10000 bytes). 
So, one possible solution is to change the _MAXLINE value to a bigger number.
Also gmail has no problem with a search this big.
"""
imaplib._MAXLINE = 400000

# Connection object for gmail inbox
conn = open_connection()

try :
	#Selecting the inbox from which mails will be fetched 
	conn.select('INBOX')

	#Variable to keep track of the number of unseen messages in the chosen mailbox
	unseen_msgs = 0

	#Searching mailbox for messages with UID from 2000 till the newest mail in inbox
	retcode, uids = conn.uid('SEARCH', None, 'UID 2000:*')
	
	num_of_messages = len(uids[0].split())
	last_rn_no = num_of_messages

	#print(uids)
	print(num_of_messages)
	
	# retcode indicates the success or failure of the imap request
	if retcode == "OK" :
		# header.json file will store all the required data
		with open("headers.json", mode = 'a', encoding = 'utf-8') as f :

			for num in uids[0].split() :

				# this conversion is required as the type of num is 'byte'. Also num indicates the UID of a mail.
				number = int(num)
				
				print('Processing mail #', number)
				unseen_msgs += 1

				#conn.uid() converts the arguments provided to an IMAP command to fetch the mail using the UID sepcified by num
				typ, msg_header = conn.uid('FETCH', num, '(RFC822)')

				#print(msg_header)

				for response_part in msg_header :
					if isinstance(response_part, tuple) :

						#response_part contains the required info as a byte stream. This has to be converted to a message stream.
						#This is done using the email module
						original = email.message_from_bytes(response_part[1])

						#The splicing is done as to remove the '<' and '>' from the message-id string 
						uid_msg_id_map[original['Message-ID'][1:-1]] = number  
				
						data = {}
						data['Message-ID'] = number
						data['From'] = original['From']
						data['To'] = original['To']
						data['Cc'] = original['Cc']
						data['In-Reply-To'] = original['In-Reply-To']

						if original['References'] == None:
							data['References'] = None
						else:
							uid_list = []
							"""
								Since all the references are also in string, we have to go through each string in the list of references.
								For each references string in the list, we check if we have already encountered it. In such a case, we 
								associate the the UID of the mail that had the first occurence of this string.
								If not, we just append the value 0.
								Also splicing is done for references to remove '<' and '>'
							"""
							for references in original['References'].split() :
								if not(references[1:-1] in list(uid_msg_id_map.keys())) :
									uid_msg_id_map[references[1:-1]] =  0

								uid_list.append(uid_msg_id_map[references[1:-1]])

							"""
								Each element of a list, when written into a .json file take a line each. To pretty print it we make 
								it an object of NoIndent class and use a custom encoder class called MyEncoder
							"""
							data['References'] = NoIndent(uid_list)

			
						json.dump(data, f, cls=MyEncoder, indent=1)
						f.write("\n") 

			#Marking all message as seen
			typ, msg_header = conn.uid('STORE', num, '+FLAGS', '\\Seen')
			
			f.close()
	print(unseen_msgs)
finally :
	try :
		conn.close()
	except :
		pass
	conn.logout()

#print(uid_msg_id_map)
# We are also storing the uid map in a separate json file.
with open("uid_map.json", mode = 'a', encoding = 'utf-8') as f :
	json.dump(uid_msg_id_map, f, indent=1)
	f.close() 
