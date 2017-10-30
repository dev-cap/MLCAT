from util.read import *
import json


def get(json_filename, output_filename, active_score, passive_score, write_to_file=True):
    """

    :param json_data: The JSON file containing the headers.
    :param output_filename: Stores authors' email address,score and rank.
    :param active_score: Score for direct mail receipents.
    :param passive_score: Score for receipents through CC.
    :return: Sorted author scores.
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

    if not ignore_lat:
        with open(json_filename, 'r') as json_file:
            for chunk in lines_per_n(json_file, 9):
                json_obj = json.loads(chunk)
                json_obj['Message-ID'] = int(json_obj['Message-ID'])
                json_obj['Time'] = datetime.datetime.strptime(json_obj['Time'], "%a, %d %b %Y %H:%M:%S %z")
                if time_lbound <= json_obj['Time'] < time_ubound:
                    # print("\nFrom", json_obj['From'], "\nTo", json_obj['To'], "\nCc", json_obj['Cc'])
                    from_addr = email_re.search(json_obj['From'])
                    json_obj['From'] = from_addr.group(0) if from_addr is not None else json_obj['From']
                    json_obj['To'] = set(email_re.findall(json_obj['To']))
                    json_obj['Cc'] = set(email_re.findall(json_obj['Cc'])) if json_obj['Cc'] is not None else None
                    # print("\nFrom", json_obj['From'], "\nTo", json_obj['To'], "\nCc", json_obj['Cc'])
                    json_data[json_obj['Message-ID']] = json_obj
    else:
        lone_author_threads = get_lone_author_threads(False)
        with open(json_filename, 'r') as json_file:
            for chunk in lines_per_n(json_file, 9):
                json_obj = json.loads(chunk)
                json_obj['Message-ID'] = int(json_obj['Message-ID'])
                if json_obj['Message-ID'] not in lone_author_threads:
                    json_obj['Time'] = datetime.datetime.strptime(json_obj['Time'], "%a, %d %b %Y %H:%M:%S %z")
                    if time_lbound <= json_obj['Time'] < time_ubound:
                        # print("\nFrom", json_obj['From'], "\nTo", json_obj['To'], "\nCc", json_obj['Cc'])
                        from_addr = email_re.search(json_obj['From'])
                        json_obj['From'] = from_addr.group(0) if from_addr is not None else json_obj['From']
                        json_obj['To'] = set(email_re.findall(json_obj['To']))
                        json_obj['Cc'] = set(email_re.findall(json_obj['Cc'])) if json_obj['Cc'] is not None else None
                        # print("\nFrom", json_obj['From'], "\nTo", json_obj['To'], "\nCc", json_obj['Cc'])
                        json_data[json_obj['Message-ID']] = json_obj
    print("JSON data loaded.")

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

