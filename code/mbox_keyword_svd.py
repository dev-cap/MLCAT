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


keyword_clusters_svd()
keyword_clusters_lsa()