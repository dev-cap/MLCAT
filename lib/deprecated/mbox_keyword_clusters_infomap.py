import mailbox

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer

from input.mbox.keyword_digest import get_message_body
from util import custom_stopwords
from util.read import *


def get_author_clustering_infomap(tree_filename="infomap/output/"+"author_graph.tree"):
    """

        :param tree_filename:
        :return:
        """
    current_module = 1
    authors_in_module = dict()
    with open(tree_filename, 'r') as tree_file:
        for line in tree_file:
            if line[0] == '#':
                continue
            current_module = int(line[:line.index(":")])
            authors_in_module[line[line.index("\"") + 1:line.rindex("\"")]] = current_module
    return authors_in_module, current_module


def generate_td_matrix_clusters(filename):

    english_stopwords = set(stopwords.words('english')) | custom_stopwords.common_words | custom_stopwords.custom_words
    email_re = re.compile(r'[\w\.-]+@[\w\.-]+')
    wnl = WordNetLemmatizer()

    print("Reading messages from MBOX file...")
    mailbox_obj = mailbox.mbox(filename)

    print("Getting cluster data from Infomap...")
    author_clusters, max_module = get_author_clustering_infomap()
    keywords_list = [list() for x in range(max(author_clusters.values()) + 1)]

    i = 0  # Number of emails processed
    for message in mailbox_obj:
        temp = email_re.search(message['From'])
        from_addr = temp.group(0) if temp is not None else message['From']
        if from_addr not in author_clusters.keys():
            continue
        msg_body = get_message_body(message)
        if from_addr is None:
            from_addr = message['From']
        msg_tokens = [x.lower() for x in re.sub('\W+', ' ', msg_body).split() if 2 < len(x) < 30]
        # Toggle comment below if numbers and underscores should also be removed.
        # msg_tokens = [x for x in re.sub('[^a-zA-Z]+', ' ', msg_body).split() if 2 < len(x) < 30]

        msg_tokens = [wnl.lemmatize(x) for x in msg_tokens if not x.isdigit() and x not in from_addr]
        msg_tokens = [x for x in msg_tokens if x not in english_stopwords]

        keywords_list[author_clusters[from_addr]].extend(msg_tokens)

        i += 1
        if not i % 10000:
            print(i, "of", len(mailbox_obj), "messages processed.")

    for num in range(len(keywords_list)):
        keywords_list[num] = " ".join(keywords_list[num])

    print("Performing tf-idf analysis on the term-document matrix...")
    vectorizer = TfidfVectorizer(analyzer='word', stop_words=english_stopwords, min_df=1)
    tfidf_matrix = vectorizer.fit_transform(keywords_list).toarray()
    feature_names = vectorizer.get_feature_names()
    # term_document_matrix = np.zeros((len(feature_names), max_module), dtype=float)

    for author_cluster_no in range(1, max_module+1):
        if max(tfidf_matrix[author_cluster_no]) > 0 and len(keywords_list[author_cluster_no]) > 99:
            # for i in range(len(tfidf_matrix[author_cluster_no])):
                # term_document_matrix[i][author_cluster_no] = tfidf_matrix[author_cluster_no][i]
            indices = tfidf_matrix[author_cluster_no].argsort()[-10:][::-1]
            print("Infomap Cluster:", author_cluster_no)
            try:
                for i in indices:
                    print(feature_names[i], "(", tfidf_matrix[author_cluster_no][i], ")", end="; ")
            except:
                pass
            finally:
                print("\n-----\n")

    # print(term_document_matrix.shape)
    # np.savetxt("keywords_clusters_infomap.csv", term_document_matrix, delimiter=",")
    # with open("feature_names.txt", 'w') as file_handler:
    #     for item in feature_names:
    #         file_handler.write("{},".format(item))

    # return term_document_matrix, feature_names

generate_td_matrix_clusters("lkml.mbox")