from lib.analysis.author.curve_fitting import generate_crt_curve_fits
from lib.analysis.author import ranking
from lib.analysis.author.time_statistics import conversation_refresh_times
from lib.analysis.author.wh_table import generate_wh_table_authors
from lib.analysis.thread.hypergraph import generate_hyperedge_distribution
from lib.input.mbox.keyword_clustering import generate_kmeans_clustering
from lib.input.mbox.keyword_digest import generate_keyword_digest
from lib.analysis.author.community import vertex_clustering

# mailbox_list = ['lkml', 'opensuse-kernel', 'opensuse-features', 'opensuse', 'opensuse-bugs', 'opensuse-factory', 'sakai-devel']
mailbox_list = ['opensuse-kernel']

for mailbox in mailbox_list:
    # Define directories
    foldername = "./data/" + mailbox + '/'
    mbox_filename = './data/' + mailbox + '/mbox/' + mailbox + '.mbox'
    headers_filename = foldername + '/json/headers.json'
    nodelist_filename = foldername + '/tables/graph_nodes.csv'
    edgelist_filename = foldername + '/tables/graph_edges.csv'
    thread_uid_filename = foldername + '/json/thread_uid_map.json'
    author_uid_filename = foldername + '/json/author_uid_map.json'

    print("Processing Mailbox:", mailbox)

    vertex_clustering(headers_filename, nodelist_filename, edgelist_filename, foldername)
    generate_hyperedge_distribution(nodelist_filename, edgelist_filename, headers_filename, foldername)
    generate_keyword_digest(mbox_filename, output_filename=foldername+"/author_keyword_digest.txt", author_uid_filename=author_uid_filename,
                            json_filename=headers_filename, top_n=250, console_output=False)
    ranking.get(headers_filename, output_filename=foldername+"/tables/author_ranking.csv", active_score=2, passive_score=1)
    generate_wh_table_authors(nodelist_filename, edgelist_filename, foldername+'/tables/wh_table_authors.csv')
    conversation_refresh_times(headers_filename, nodelist_filename, edgelist_filename, foldername+'plots', plot=True)
    generate_kmeans_clustering(mbox_filename, author_uid_filename=author_uid_filename, json_filename=headers_filename,
                               output_filename=foldername+"/json/kmeans_clustering.json", top_n=250)

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
                (a, b, c), rmsd = generate_crt_curve_fits(foldername + '/curve_fit/' + month + '_' + str(year) + '/')
                monthly_curve_fit_coeffs.append((month, year, a, b, c, rmsd))

        outstr = conversation_refresh_times(headers_filename, nodelist_filename, edgelist_filename,
                                   foldername=foldername + '/curve_fit/' + 'FULL_' + str(year) + '/',
                                   time_lbound="01 Jan " + str(year) + " 00:00:00 +0000",
                                   time_ubound="31 Dec " + str(year) + " 23:59:59 +0000")
        if outstr is None:
            (a, b, c), rmsd = generate_crt_curve_fits(foldername + '/curve_fit/' + 'FULL_' + str(year) + '/')
            yearly_curve_fit_coeffs.append((year, a, b, c, rmsd))

    with open(foldername + '/curve_fit/' + 'crt_curve_fit_coefficients.csv', 'w') as csv_file:
        csv_file.write("Monthly CRT Curve-fit Coefficients:\nMonth, Year, A, B, C, RMSD\n")
        for month, year, a, b, c, rmsd in monthly_curve_fit_coeffs:
            csv_file.write(str(year) + ',' + month + ',' + str(a) + ',' + str(b) + ',' + str(c) + ',' + str(rmsd) + '\n')
        csv_file.write("\nYearly CRT Curve-fit Coefficients:\nMonth, Year, A, B, C, RMSD\n")
        for year, a, b, c, rmsd in yearly_curve_fit_coeffs:
            csv_file.write(str(year) + ',' + ',' + str(a) + ',' + str(b) + ',' + str(c) + ',' + str(rmsd) + '\n')
        csv_file.close()
    print("----------------")
