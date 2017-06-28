import traceback

from analysis.thread.graph.edge_list import generate_edge_list
from input.check_headers import *
from input.data_cleanup import remove_invalid_references
from input.mbox.mbox_hdr import extract_mail_header


# Test Data Handling Module
def driver_data_handling(mailbox_list):
    for mailbox in mailbox_list:
        try:
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
            remove_duplicate_headers(json_header_filename=unclean_headers_filename)
            remove_invalid_references(input_json_filename=unclean_headers_filename, output_json_filename=clean_headers_filename, ref_toggle=True)
            generate_edge_list(nodelist_filename=nodelist_filename, edgelist_filename=edgelist_filename, json_filename=unclean_headers_filename)

        except Exception as inst:
            return traceback.print_exc()
            return inst
    return "Successful"


def test_data_handling():
    mailbox_list = ['opensuse-kernel']
    assert driver_data_handling(mailbox_list) == "Successful"


def driver_author_analysis(mailbox_list):
    # TODO: Add test cases for analysis.thread here
    return "Successful"


def test_author_analysis():
    mailbox_list = ['sakai-devel']
    assert driver_author_analysis(mailbox_list) == "Successful"


def driver_thread_analysis(mailbox_list):
    # TODO: Add test cases for analysis.thread here
    return "Successful"


def test_thread_analysis():
    mailbox_list = ['sakai-devel']
    assert driver_author_analysis(mailbox_list) == "Successful"


mailbox_list_thread_analysis = ['sakai-devel']
test_data_handling()