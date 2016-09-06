# mailbox_list = ['lkml', 'opensuse-bugs', 'opensuse', 'opensuse-kernel', 'incubator-depot-cvs', 'opensuse-features']
mailbox_list = ['lkml', 'opensuse-kernel', 'opensuse-features']

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

    print("----------------")