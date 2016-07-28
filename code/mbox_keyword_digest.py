import mailbox
import json
import numpy as np
from nltk.corpus import stopwords
from ext import custom_stopwords
from util.read_utils import *
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer


def save_sparse_csr(filename, array):
    np.savez(filename,data = array.data ,indices=array.indices,
             indptr =array.indptr, shape=array.shape )


def get_message_body(message):
    """

    :param message:
    :return:
    """
    msg_body = None
    if message.is_multipart():
        for part in message.walk():
            if part.is_multipart():
                for subpart in part.walk():
                    if subpart.get_content_type() == 'text/plain':
                        msg_body = subpart.get_payload(decode=False)
            elif part.get_content_type() == 'text/plain':
                msg_body = part.get_payload(decode=False)
    elif message.get_content_type() == 'text/plain':
        msg_body = message.get_payload(decode=False)

    msg_body = msg_body.splitlines()
    for num in range(len(msg_body)):
        if msg_body[num]:
            if msg_body[num] == "---":
                msg_body = msg_body[:num]
                break
            if msg_body[num][0] == '>' or msg_body[num][0] == '+' or msg_body[num][0] == '-' or msg_body[num][0] == '@':
                msg_body[num] = ""
                if num > 0:
                    msg_body[num - 1] = ""
            elif msg_body[num][:3] == "Cc:":
                msg_body[num] = ""
            elif msg_body[num][:14] == "Signed-off-by:":
                msg_body[num] = ""
            elif msg_body[num][:9] == "Acked-by:":
                msg_body[num] = ""
            elif msg_body[num][:5] == "From:":
                msg_body[num] = ""
            elif msg_body[num][:10] == "Tested-by:":
                msg_body[num] = ""
            elif msg_body[num][:12] == "Reported-by:":
                msg_body[num] = ""
            elif msg_body[num][:12] == "Reviewed-by:":
                msg_body[num] = ""
            elif msg_body[num][:5] == "Link:":
                msg_body[num] = ""
            elif msg_body[num][:13] == "Suggested-by:":
                msg_body[num] = ""
    msg_body = [x.strip() for x in msg_body]
    msg_body = [x for x in msg_body if x != ""]
    msg_body = '\n'.join(msg_body)
    return msg_body


def generate_keyword_digest(filename, console_output=True):
    """
    From the .MBOX file, this function extracts the email content is extracted using two predefined classes
    available in the Python Standard Library: Mailbox and Message. Feature vectors are created for all the authors
    by obtaining meaningful words from the mail content, after removing the stop words, using NLTK libraries.
    The words obtained are transformed using stemming or lemmatization before adding these words to the word list of
    the corresponding authors. A matrix is created out of these word lists such that row set is the union of terms of
    all the authors and the column set contains the authors. If a term does not appear in a document, the corresponding
    matrix entry would be zero. The resulting matrix is called term-document matrix. Then tf-idf analysis is performed
    on the term-document matrix. Finally the top-10 words of each author is listed by their weight values.
    :param filename: Contains the absolute or relative address of the MBOX file to be opened
    :return: Term Document Matrix: The columns of the matrix are the users and the rows of the matrix are the keywords.
    Each entry corresponds to the tf-idf normalized coefficient of the keyword for a user. If a keyword is not present
    in the top-10 keywords of a user, then the corresponding matrix entry would be zero. Also returns the feature names.
    """
    english_stopwords = set(stopwords.words('english')) | custom_stopwords.common_words | custom_stopwords.custom_words
    email_re = re.compile(r'[\w\.-]+@[\w\.-]+')
    wnl = WordNetLemmatizer()

    print("Reading messages from MBOX file...")
    mailbox_obj = mailbox.mbox(filename)
    print("Reading author UIDs from JSON file...")
    with open('author_uid_map.json', 'r') as map_file:
        author_uid_map = json.load(map_file)
        map_file.close()
    keywords_list = [list() for x in range(max(author_uid_map.values())+1)]
    i = 0 # Number of emails processed
    for message in mailbox_obj:
        temp = email_re.search(message['From'])
        from_addr = temp.group(0) if temp is not None else message['From']
        if from_addr not in author_uid_map.keys():
            continue
        msg_body = get_message_body(message)
        if from_addr is None:
            from_addr = message['From']
        msg_tokens = [x.lower() for x in re.sub('\W+', ' ', msg_body).split() if 2 < len(x) < 30]
        # Toggle comment below if numbers and underscores should also be removed.
        # msg_tokens = [x for x in re.sub('[^a-zA-Z]+', ' ', msg_body).split() if 2 < len(x) < 30]

        msg_tokens = [wnl.lemmatize(x) for x in msg_tokens if not x.isdigit() and x not in from_addr]
        msg_tokens = [x for x in msg_tokens if x not in english_stopwords]
        keywords_list[author_uid_map[from_addr]].extend(msg_tokens)
        if not console_output:
            i += 1
            if not i % 1000:
                print(i, "of", len(mailbox_obj), "messages processed.")

    for num in range(len(keywords_list)):
        keywords_list[num] = " ".join(keywords_list[num])

    print("Performing tf-idf analysis on the term-document matrix...")
    vectorizer = TfidfVectorizer(analyzer='word', stop_words=english_stopwords, min_df=1)
    tfidf_matrix = vectorizer.fit_transform(keywords_list).toarray()
    feature_names = vectorizer.get_feature_names()
    term_document_matrix = np.zeros((len(feature_names), len(author_uid_map)), dtype=float)
    for author_email, author_uid in author_uid_map.items():
        if max(tfidf_matrix[author_uid]) > 0 and len(keywords_list[num]) > 99:
            try:
                for i in len(tfidf_matrix[author_uid]):
                    term_document_matrix[i][author_uid] = tfidf_matrix[author_uid][i]
                indices = tfidf_matrix[author_uid].argsort()[-10:][::-1]
                if console_output:
                    print(author_email)
                    for i in indices:
                        print(feature_names[i], "(", tfidf_matrix[author_uid][i], ")", end="; ")
            except:
                pass
            finally:
                if console_output:
                    print("\n-----\n")

    return term_document_matrix, feature_names

# generate_keyword_digest("lkml.mbox")