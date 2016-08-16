import mailbox
import json
import numpy as np
from util.read_utils import *
from sklearn.utils.extmath import randomized_svd
from mbox_keyword_digest import generate_keyword_digest


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

# keyword_clusters_svd()
# keyword_clusters_lsa()
calculate_percentile()