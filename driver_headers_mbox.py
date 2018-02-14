
import os.path
from lib.input.check_headers import *
from lib.input.mbox.mbox_hdr import extract_mail_header
from lib.input.data_cleanup import remove_invalid_references
from lib.analysis.author.edge_list import generate_edge_list
import configparser
config = configparser.ConfigParser()
config.read('config.ini')


mailbox_list = [d for d in os.listdir('data') if os.path.isdir(os.path.join('data', d))]
mailbox_list = ['lkml', 'opensuse', 'opensuse-bugs', 'opensuse-factory', 'opensuse-features', 'opensuse-kernel', 'sakai-devel']
mailbox_list = ['opensuse-kernel']
for mailbox in mailbox_list:
    # Define directories
    mbox_filename = config['param_paths']['foldername'] + mailbox + '/mbox/' + mailbox + '.mbox'
    clean_headers_filename = config['param_paths']['foldername'] + mailbox + config['param_paths']['clean_headers_path']
    headers_filename = config['param_paths']['foldername'] + mailbox +config['param_paths']['headers_path']
    nodelist_filename = config['param_paths']['foldername'] + mailbox  +config['param_paths']['nodelist_path']
    edgelist_filename = config['param_paths']['foldername'] + mailbox +config['param_paths']['edgelist_path']
    thread_uid_filename = config['param_paths']['foldername']+ mailbox +config['param_paths']['thread_uid_path']
    author_uid_filename = config['param_paths']['foldername']+ mailbox +config['param_paths']['author_uid_path']
    print("Processing Mailbox:", mailbox)
    extract_mail_header(mbox_filename=mbox_filename, json_filename=headers_filename,
                       thread_uid_filename=thread_uid_filename, author_uid_filename=author_uid_filename)
    last_uid = check_validity(False, json_header_filename=headers_filename)
    print("Last valid UID in JSON file:", last_uid)
    # remove_duplicate_headers(json_header_filename=unclean_headers_filename)
    # remove_invalid_references(input_json_filename=unclean_headers_filename, output_json_filename=clean_headers_filename, ref_toggle=True)
    # generate_edge_list(nodelist_filename=nodelist_filename, edgelist_filename=edgelist_filename, threads_json_filename=clean_headers_filename)
    print("----------------")
    

