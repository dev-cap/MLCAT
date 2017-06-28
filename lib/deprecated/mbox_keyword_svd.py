import random

import numpy as np
from sklearn.feature_selection import chi2
from sklearn.utils.extmath import randomized_svd

from input.mbox.keyword_digest import generate_keyword_digest


def keyword_clusters_svd():
    top_authors_index, term_document_matrix, feature_names = generate_keyword_digest("lkml.mbox", top_n=1000, console_output=False)
    sigma = np.linalg.svd(term_document_matrix, compute_uv=False, full_matrices=True)
    np.savetxt("authors_keyword_svd.txt", sigma, delimiter=",", header=str(feature_names)[-1:1])
    sigma = np.diag(sigma)
    np.savetxt("authors_keyword_svd.csv", sigma, delimiter=",", header=str(feature_names)[-1:1])


def keyword_clusters_lsa():
    top_authors_index, term_document_matrix, feature_names = generate_keyword_digest("lkml.mbox", top_n=1000, console_output=False)
    u, sigma, v = randomized_svd(term_document_matrix, n_components=100)
    sigma = np.diag(sigma)
    np.savetxt("authors_keyword_lsa.csv", sigma, delimiter=",", header=str(feature_names)[-1:1])


def calculate_percentile(filename="authors_keyword_svd.txt", percentile=0.95):
    diag_elements = list()
    with open(filename, 'r') as input_file:
        for line in input_file:
            diag_elements.append(float(line))
    denominator = sum([x**2 for x in diag_elements])
    numerator = 0
    for index in range(len(diag_elements)):
        numerator += diag_elements[index]**2
        if numerator/denominator>=percentile**2:
            break
    print("95th Percentile:", index)


def calculate_chi2():
    top_authors_index, term_document_matrix, feature_names = generate_keyword_digest("lkml.mbox", top_n=1000, console_output=False)

    # Remove features that are empty: All TF-IDF values are zero
    for term_no in range(len(term_document_matrix)):
        term = term_document_matrix[term_no]
        to_remove = 1
        for doc_no in range(len(term)):
            doc = term[doc_no]
            if doc != 0:
                to_remove = 0
                break
        if to_remove:
            term_document_matrix[term_no][0] = -100
    print(term_document_matrix.shape)
    term_no = len(term_document_matrix) - 1

    while 0 <= term_no < len(term_document_matrix):
        if term_document_matrix[term_no][0] == -100:
            try:
                term_document_matrix = np.delete(term_document_matrix, term_no, axis=0)
                feature_names.pop(term_no)
            except:
                print("Error", term_no, len(feature_names), len(term_document_matrix))
        term_no -= 1
    # np.savetxt("td.csv", term_document_matrix, delimiter=",", header=str(feature_names)[-1:1])
    document_term_matrix = term_document_matrix.T
    for term_no in range(len(document_term_matrix)):
        term = document_term_matrix[term_no]
        to_remove = 1
        for doc_no in range(len(term)):
            doc = term[doc_no]
            if doc != 0:
                to_remove = 0
                break
        if to_remove:
            term_document_matrix[term_no][0] = -100

    print(term_document_matrix.shape)
    term_no = len(document_term_matrix) - 1
    while 0 <= term_no < len(document_term_matrix):
        if document_term_matrix[term_no][0] == -100:
            try:
                document_term_matrix = np.delete(document_term_matrix, term_no, axis=0)
            except:
                print("Error", term_no, len(feature_names), len(document_term_matrix))
        term_no -= 1

    print(document_term_matrix.shape)
    for i in range(len(document_term_matrix)):
        for j in range(len(document_term_matrix[i])):
            document_term_matrix[i][j] += random.uniform(0, 0.1)
    target = np.zeros((len(document_term_matrix), 1), dtype='float64')
    for i in range(len(target)):
        target[i] = i

    chi2_score, p_val = chi2(document_term_matrix, target)
    with open("keyword_digest_chi2_scores.csv", 'w') as out_file:
        out_file.write("Keyword,Chi^2 Score\n")
        for name, score in zip(feature_names, chi2_score):
            try:
                out_file.write(name + "," + str(score) + "\n")
            except:
                pass
    # Uncomment to save as figure:
    # figure(figsize=(12, 6))
    # wscores = zip(feature_names, chi2_score)
    # wchi2 = sorted(wscores, key=lambda x: x[1])
    # topchi2 = list(zip(*wchi2[-25:]))
    # x = range(len(topchi2[1]))
    # labels = topchi2[0]
    # barh(x, topchi2[1], align='center', alpha=.2, color='g')
    # plot(topchi2[1], x, '-o', markersize=2, alpha=.8, color='g')
    # yticks(x, labels)
    # xlabel('$\chi^2$')
    # savefig("chi2.png")

# keyword_clusters_svd()
# keyword_clusters_lsa()
# calculate_percentile()
calculate_chi2()