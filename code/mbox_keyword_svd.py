import mailbox
import json
import numpy as np
from util.read_utils import *
from sklearn.utils.extmath import randomized_svd
from mbox_keyword_digest import generate_keyword_digest


def keyword_clusters_svd():
    term_document_matrix, feature_names = generate_keyword_digest("lkml.mbox", console_output=False)
    sigma = np.linalg.svd(term_document_matrix, compute_uv=False)
    for i in sigma:
        print(i, end  =", ")


def keyword_clusters_lsa():
    term_document_matrix, feature_names = generate_keyword_digest("lkml.mbox", console_output=False)
    u, sigma, v = randomized_svd(term_document_matrix, n_components=100)
    for i in sigma:
        print(i, end  =", ")

# keyword_clusters_lsa()
keyword_clusters_svd()