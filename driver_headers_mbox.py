
import os.path
import sys
from lib.input.check_headers import *
from lib.input.mbox.mbox_hdr import extract_mail_header
from lib.input.data_cleanup import remove_invalid_references
from lib.analysis.author.edge_list import generate_edge_list
from lib.mlcatconfig.config import Config


mailbox_list = [d for d in os.listdir('data') if os.path.isdir(os.path.join('data', d))]
mailbox_list = ['lkml', 'opensuse', 'opensuse-bugs', 'opensuse-factory', 'opensuse-features', 'opensuse-kernel', 'sakai-devel']
mailbox_list = ['opensuse-kernel']
for mailbox in mailbox_list:
    
    path=os.path.abspath("lib/mlcatconfig/mlcat.cfg")
    path_ob= Config(mailbox)
    path_ob.read(path)
    path_ob.createVariables();
   
    
    print("Processing Mailbox:", mailbox)
    extract_mail_header(mbox_filename=path_ob.mbox_filename, json_filename=path_ob.headers_filename,
                       thread_uid_filename=path_ob.thread_uid_filename, author_uid_filename=path_ob.author_uid_filename)
    obj=CheckHeaders()
    last_uid = obj.check_validity(False, json_header_filename=path_ob.headers_filename)
    print("Last valid UID in JSON file:", last_uid)
    
    
    
    # obj.remove_duplicate_headers(json_header_filename=unclean_headers_filename)
    # remove_invalid_references(input_json_filename=unclean_headers_filename, output_json_filename=clean_headers_filename, ref_toggle=True)
    # generate_edge_list(nodelist_filename=nodelist_filename, edgelist_filename=edgelist_filename, threads_json_filename=clean_headers_filename)
    print("----------------")
    
    
    

