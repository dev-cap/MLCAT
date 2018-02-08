import mailbox
import json
import datetime
from util.read import *


def extract_mail_header(mbox_filename, json_filename='headers.json', thread_uid_filename='thread_uid_map.json', author_uid_filename='author_uid_map.json'):
    """
    From the .MBOX file, this function extracts the header information is extracted using two predefined classes
    available in the Python Standard Library: Mailbox and Message, for accessing and manipulating on-disk mailboxes
    and the messages they contain respectively. The headers are then saved to a JSON file. an unique Message-ID is
    provided to each message in the .MBOX file in the ascending order of their arrival times. The mapping between
    the UIDs and Message-IDs are stored in another JSON file.
    
    :param mbox_filename: Contains the absolue or relative address of the file to be opened.
    :param json_filename: The JSON file in which the extracted headers are stored.
    :param thread_uid_filename: Contains a mapping between threads and UIDs.
    :param author_uid_filename: Contains a mapping between authors and UIDs.
    """
    print("Reading messages from MBOX file...")
    mailbox_obj = mailbox.mbox(mbox_filename)
    author_uid_map = dict()
    msg_hdr_list = list()
    uid_msg_id_map = dict()
    email_re = re.compile(r'[\w\.-]+@[\w\.-]+')
    for msg_obj in mailbox_obj:
        msg_data = dict()
        if msg_obj.get('Message-ID') is None:
            continue
        msg_data['Message-ID'] = None
        msg_data['From'] = str(msg_obj.get('From'))
        msg_data['To'] = str(msg_obj.get('To'))
        if msg_data['To'] == 'None' or msg_data['From'] == 'None':
            continue
        msg_data['Cc'] = str(msg_obj.get('Cc'))
        from_addr = email_re.search(msg_data['From'])
        msg_data['From_iter'] = from_addr.group(0) if from_addr is not None else msg_data['From']
        msg_data['To_iter'] = set(email_re.findall(msg_data['To']))
        msg_data['Cc_iter'] = set(email_re.findall(msg_data['Cc'])) if msg_data['Cc'] is not None else None
        msg_data['Time'] = get_utc_time(msg_obj.get('Date'))
        if msg_data['Time'] == 'Error':
            continue
        msg_data['In-Reply-To'] = str(msg_obj.get('In-Reply-To'))
        msg_data['References'] = str(msg_obj.get('References'))
        msg_hdr_list.append((msg_data, str(msg_obj.get('Message-ID'))[1:-1]))

    msg_count = 1
    author_count = 1
    msg_hdr_list.sort(key=lambda msg: datetime.datetime.strptime(msg[0]['Time'], "%a, %d %b %Y %H:%M:%S %z"))
    for msg_data, uid in msg_hdr_list:
        msg_data['Message-ID'] = msg_count
        uid_msg_id_map[uid] = msg_count
        if msg_data['Cc'] is None:
            addr_list = msg_data['To_iter']
        else:
            addr_list = msg_data['To_iter'] | msg_data['Cc_iter']
        addr_list.add(msg_data['From_iter'])
        for to_address in addr_list:
            if author_uid_map.get(to_address, None) is None:
                author_uid_map[to_address] = author_count
                author_count += 1
        msg_count += 1

    print("Writing mail headers to JSON file...")
    with open(json_filename, mode='w', encoding='utf-8') as json_file:
        for msg_data, uid in msg_hdr_list:
            msg_data.pop('To_iter')
            msg_data.pop('From_iter')
            msg_data.pop('Cc_iter')
            if not msg_data['In-Reply-To'] == 'None':
                msg_data['In-Reply-To'] = uid_msg_id_map.get(msg_data['In-Reply-To'][1:-1], 0)
                if msg_data['In-Reply-To'] > msg_data['Message-ID']:
                    msg_data['In-Reply-To'] = 0
            else:
                msg_data['In-Reply-To'] = 0
            if msg_data['References']:
                ref_list = list()
                for reference in msg_data['References'].split(','):
                    ref_list.append(uid_msg_id_map.get(reference.strip()[1:-1], 0))
                msg_data['References'] = str(ref_list)[1:-1]
            json.dump(msg_data, json_file, indent=1)
            json_file.write("\n")
        json_file.close()

    print("Number of messages processed:", msg_count-1)
    print("Writing threads UID map to file...")
    with open(thread_uid_filename, mode='w', encoding='utf-8') as map_file:
        json.dump(uid_msg_id_map, map_file, indent=1)
        map_file.close()

    print("Writing authors UID map to file...")
    with open(author_uid_filename, mode='w', encoding='utf-8') as map_file:
        json.dump(author_uid_map, map_file, indent=1)
        map_file.close()
