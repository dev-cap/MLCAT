from hypergraph_statistics import generate_hyperedge_distribution
from mbox_keyword_digest import generate_keyword_digest
from author_ranking import generate_author_ranking
from wh_table_authors import generate_wh_table_authors
from time_statistics_authors import conversation_refresh_times
from mbox_keywords_kmeans_clustering import generate_kmeans_clustering
from time_statistics_curve_fitting import generate_crt_curve_fits
import os.path

mailbox_list = [d for d in os.listdir('data') if os.path.isdir(os.path.join('data', d))]
mailbox_list = ['lkml', 'opensuse-kernel', 'opensuse-features', 'opensuse', 'opensuse-bugs', 'opensuse-factory']

for mailbox in mailbox_list:
    # Define directories
    foldername = "./data/" + mailbox
    mbox_filename = './data/' + mailbox + '/mbox/' + mailbox + '.mbox'
    headers_filename = foldername + '/json/headers.json'
    nodelist_filename = foldername + '/tables/graph_nodes.csv'
    edgelist_filename = foldername + '/tables/graph_edges.csv'
    thread_uid_filename = foldername + '/json/thread_uid_map.json'
    author_uid_filename = foldername + '/json/author_uid_map.json'

    print("Processing Mailbox:", mailbox)
    generate_hyperedge_distribution(nodelist_filename, edgelist_filename, headers_filename, foldername)
    generate_keyword_digest(mbox_filename, output_filename=foldername+"/author_keyword_digest.txt", author_uid_filename=author_uid_filename,
                            json_filename=headers_filename, top_n=250, console_output=False)
    generate_author_ranking(headers_filename, output_filename=foldername+"/tables/author_ranking.csv", active_score=2, passive_score=1)
    generate_wh_table_authors(nodelist_filename, edgelist_filename, foldername+'/tables/wh_table_authors.csv')
    conversation_refresh_times(headers_filename, nodelist_filename, edgelist_filename, foldername)
    generate_kmeans_clustering(mbox_filename, author_uid_filename=author_uid_filename, json_filename=headers_filename, output_filename=foldername+"/json/kmeans_clustering.json", top_n=250)

    # For a range of months from Jan 2010 to Dec 2016, generate CL, RT curve fits
    yearly_curve_fit_coeffs = list()
    monthly_curve_fit_coeffs = list()
    for year in range(2015, 2017):
        for month in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']:
            if month in {'Jan', 'Mar', 'May', 'Jul', 'Aug', 'Oct', 'Dec'}:
                max_day = 31
            elif month == 'Feb':
                max_day = 28
            else:
                max_day = 30
            outstr = conversation_refresh_times(headers_filename, nodelist_filename, edgelist_filename,
                                        foldername=foldername + '/curve_fit/' + month + '_' + str(year) + '/',
                                        time_lbound="01 " + month + " " + str(year) + " 00:00:00 +0000",
                                        time_ubound=str(max_day) + " " + month + " " + str(year) + " 23:59:59 +0000")
            if outstr is None:
                a, b, c = generate_crt_curve_fits(foldername + '/curve_fit/' + month + '_' + str(year) + '/')
                monthly_curve_fit_coeffs.append((month, year, a, b, c))

        outstr = conversation_refresh_times(headers_filename, nodelist_filename, edgelist_filename,
                                   foldername=foldername + '/curve_fit/' + 'FULL_' + str(year) + '/',
                                   time_lbound="01 Jan " + str(year) + " 00:00:00 +0000",
                                   time_ubound="31 Dec " + str(year) + " 23:59:59 +0000")
        if outstr is None:
            a, b, c = generate_crt_curve_fits(foldername + '/curve_fit/' + 'FULL_' + str(year) + '/')
            yearly_curve_fit_coeffs.append((year, a, b, c))

    print("----------------")
