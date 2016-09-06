from heatmap_message_activity import generate_message_activity_heatmaps


# mailbox_list = ['lkml', 'opensuse-bugs', 'opensuse', 'opensuse-kernel', 'incubator-depot-cvs', 'opensuse-features']
mailbox_list = ['opensuse-kernel', 'opensuse-features']

for mailbox in mailbox_list:
    # Define directories
    foldername = "./data/" + mailbox
    clean_headers_filename = foldername + '/json/clean_data.json'
    nodelist_filename = foldername + '/tables/graph_nodes.csv'
    edgelist_filename = foldername + '/tables/graph_edges.csv'
    thread_uid_filename = foldername + '/json/thread_uid_map.json'
    author_uid_filename = foldername + '/json/author_uid_map.json'

    print("Analyzing Thread Network in Mailbox:", mailbox)
    generate_message_activity_heatmaps(clean_headers_filename=clean_headers_filename, foldername=foldername)
    print("----------------")