import os.path

from lib.input.check_headers import *
from lib.input.mbox.mbox_hdr import extract_mail_header
from lib.input.data_cleanup import remove_invalid_references
from lib.analysis.author.edge_list import generate_edge_list

mailbox_list = [d for d in os.listdir('data') if os.path.isdir(os.path.join('data', d))]
mailbox_list = ['lkml', 'opensuse', 'opensuse-bugs', 'opensuse-factory', 'opensuse-features', 'opensuse-kernel', 'sakai-devel']
mailbox_list = ['opensuse-kernel']

for mailbox in mailbox_list:
    # Define directories
    mbox_filename = './data/' + mailbox + '/mbox/' + mailbox + '.mbox'
    clean_headers_filename = './data/' + mailbox + '/json/clean_data.json'
    unclean_headers_filename = './data/' + mailbox + '/json/headers.json'
    nodelist_filename = './data/' + mailbox + '/tables/graph_nodes.csv'
    edgelist_filename = './data/' + mailbox + '/tables/graph_edges.csv'
    thread_uid_filename = './data/' + mailbox + '/json/thread_uid_map.json'
    author_uid_filename = './data/' + mailbox + '/json/author_uid_map.json'

    print("Processing Mailbox:", mailbox)
    extract_mail_header(mbox_filename=mbox_filename, json_filename=unclean_headers_filename,
                        thread_uid_filename=thread_uid_filename, author_uid_filename=author_uid_filename)
    last_uid = check_validity(False, json_header_filename=unclean_headers_filename)
    print("Last valid UID in JSON file:", last_uid)
    # remove_duplicate_headers(json_header_filename=unclean_headers_filename)
    # remove_invalid_references(input_json_filename=unclean_headers_filename, output_json_filename=clean_headers_filename, ref_toggle=True)
    # generate_edge_list(nodelist_filename=nodelist_filename, edgelist_filename=edgelist_filename, threads_json_filename=clean_headers_filename)
    print("----------------")
