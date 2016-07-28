import mailbox
import json
import datetime
from util.read_utils import *


def extract_mail_header(filename):
    """
    From the .MBOX file, this function extracts the header information is extracted using two predefined classes
    available in the Python Standard Library: Mailbox and Message, for accessing and manipulating on-disk mailboxes
    and the messages they contain respectively. The headers are then saved to a JSOn file. an unique Message-ID is
    provided to each message in the .MBOX file in the ascending order of their arrival times. The The mapping between
    the UIDs and Message-IDs are stored in another JSON file
    :param filename: Contains the absolute or relative address of the file to be opened
    """
    print("Reading messages from MBOX file...")
    mailbox_obj = mailbox.mbox(filename)
    msg_hdr_list = list()
    uid_msg_id_map = dict()
    for msg_obj in mailbox_obj:
        msg_data = dict()
        msg_data['Message-ID'] = None
        msg_data['From'] = msg_obj.get('From')
        msg_data['To'] = msg_obj.get('To')
        msg_data['Cc'] = msg_obj.get('Cc')
        msg_data['Time'] = get_utc_time(msg_obj.get('Date'))
        msg_data['In-Reply-To'] = msg_obj.get('In-Reply-To')
        msg_data['References'] = msg_obj.get('References')
        msg_hdr_list.append((msg_data, msg_obj.get('Message-ID')[1:-1]))

    msg_count = 1
    msg_hdr_list.sort(key=lambda msg: datetime.datetime.strptime(msg[0]['Time'], "%a, %d %b %Y %H:%M:%S %z"))
    for msg_data, uid in msg_hdr_list:
        msg_data['Message-ID'] = msg_count
        uid_msg_id_map[uid] = msg_count
        msg_count +=1

    print("Number of messages processed:", msg_count-1)
    print("Writing mail headers to JSON file...")
    with open("headers.json", mode='w', encoding='utf-8') as json_file:
        for msg_data, uid in msg_hdr_list:
            if msg_data['In-Reply-To']:
                msg_data['In-Reply-To'] = uid_msg_id_map.get(msg_data['In-Reply-To'][1:-1], 0)
                if msg_data['In-Reply-To'] > msg_data['Message-ID']:
                    msg_data['In-Reply-To'] = 0
            if msg_data['References']:
                ref_list = list()
                for reference in msg_data['References'].split(','):
                    ref_list.append(uid_msg_id_map.get(reference.strip()[1:-1], 0))
                msg_data['References'] = str(ref_list)[1:-1]
            json.dump(msg_data, json_file, indent=1)
            json_file.write("\n")
        json_file.close()

    print("Writing UID map to file...")
    with open("thread_uid_map.json", mode='w', encoding='utf-8') as map_file:
        json.dump(uid_msg_id_map, map_file, indent=1)
        map_file.close()