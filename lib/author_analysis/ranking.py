from util.read_utils import *
import json


def generate_author_ranking(json_filename, output_filename, active_score, passive_score, write_to_file=True):
    """

    :param json_data:
    :param active_score:
    :param passive_score:
    :return:
    """

    # Time limit can be specified here in the form of a timestamp in one of the identifiable formats. All messages
    # that have arrived after time_ubound and before time_lbound will be ignored.
    time_ubound = None
    time_lbound = None

    # If ignore_lat is true, then messages that belong to threads that have only a single author are ignored.
    ignore_lat = False

    author_graph = nx.DiGraph()
    email_re = re.compile(r'[\w\.-]+@[\w\.-]+')
    json_data = dict()

    if time_ubound is None:
        time_ubound = time.strftime("%a, %d %b %Y %H:%M:%S %z")
    time_ubound = get_datetime_object(time_ubound)

    if time_lbound is None:
        time_lbound = "Sun, 01 Jan 2001 00:00:00 +0000"
    time_lbound = get_datetime_object(time_lbound)

    print("All messages before", time_ubound, "and after", time_lbound, "are being considered.")

    
    # call the method from read_utils
    load_json(ignore_lat, time_lbound, time_ubound, email_re, json_data, json_filename)

    author_scores = dict()
    for msg_uid, json_obj in json_data.items():
        if json_obj['Cc'] is None:
            num_cc = 0
            num_to = len(json_obj['To'])
            for to_address in json_obj['To']:
                if to_address not in author_scores.keys():
                    author_scores[to_address] = active_score
                else:
                    author_scores[to_address] += active_score
        else:
            num_cc = len(json_obj['Cc'])
            for to_address in json_obj['Cc']:
                if to_address not in author_scores.keys():
                    author_scores[to_address] = passive_score
                else:
                    author_scores[to_address] += passive_score
            num_to = len(json_obj['To'])
            for to_address in json_obj['To']:
                if to_address not in author_scores.keys():
                    author_scores[to_address] = active_score
                else:
                    author_scores[to_address] += active_score
        if json_obj['From'] not in author_scores.keys():
            author_scores[json_obj['From']] = active_score * num_to + passive_score * num_cc
        else:
            author_scores[json_obj['From']] += active_score * num_to + passive_score * num_cc
    prev_score = -1
    author_rank = 0
    sorted_author_scores = sorted(author_scores.items(), key=lambda x1: -x1[1])

    if write_to_file:
        print("Writing author ranks to a CSV file...")
        with open(output_filename, mode='w') as output_file:
            output_file.write("Email Address,Author's Score,Author's Rank\n")
            for email_addr, author_score in sorted_author_scores:
                if author_score != prev_score:
                    author_rank += 1
                prev_score = author_score
                output_file.write("{0},{1},{2}\n".format(email_addr, str(author_score),str(author_rank)))
            output_file.close()

    return sorted_author_scores


