import json
import re
import traceback
import pytz
import datetime
import time
import networkx as nx
from itertools import islice, chain


def lines_per_n(f, n):
    """
    Each json object in the headers.json file occupies a set number of lines.
    This function is used to read those set number of lines and return them.
    """
    for line in f :
        yield ''.join(chain([line], islice(f, n-1)))


def get_lone_author_threads(save_file=None, nodelist_filename='graph_nodes.csv', edgelist_filename='graph_edges.csv'):
    """
    This function returns the UID of all the nodes that belong to a thread that has only one author
    :param save_file: If True, the list of UIDs of nodes are saved to a text file
    :return: A set containing the UID of all the nodes that belong to a thread that has a single author
    """
    discussion_graph = nx.DiGraph()
    email_re = re.compile(r'[\w\.-]+@[\w\.-]+')
    lone_author_threads = set()

    # Add nodes into NetworkX graph by reading CSV file
    with open(nodelist_filename, "r") as node_file:
        for pair in node_file:
            node = pair.split(';', 2)
            from_addr = email_re.search(node[1].strip())
            from_addr = from_addr.group(0) if from_addr is not None else node[1].strip()
            discussion_graph.add_node(int(node[0]), time=node[2].strip(), sender=from_addr)
        node_file.close()

    # Add edges into NetworkX graph by reading CSV file
    with open(edgelist_filename, "r") as edge_file:
        for pair in edge_file:
            edge = pair.split(';')
            edge[0] = int(edge[0])
            edge[1] = int(edge[1])
            try:
                discussion_graph.node[edge[0]]['sender']
                discussion_graph.node[edge[1]]['sender']
                discussion_graph.add_edge(*edge)
            except KeyError:
                pass
        edge_file.close()

    for conn_subgraph in nx.weakly_connected_component_subgraphs(discussion_graph):
        thread_authors = set()
        for node, attributes in sorted(conn_subgraph.nodes_iter(data=True)):
            thread_authors.add(attributes['sender'])
        if len(thread_authors) <= 1:
            lone_author_threads.update(int(x) for x in conn_subgraph.nodes())

    if save_file is not None:
        print("Saving to lone_author_threads.txt...")
        with open("lone_author_threads.txt", 'w') as txt_file:
            for uid in sorted(lone_author_threads):
                txt_file.write(str(uid) + '\n')
    return lone_author_threads


def get_datetime_object(orig_time):
    """
    A function to convert a formatted string containing date and time from a local timezone to UTC, by taking into
    consideration multiple formats of the input parameter and then return the corresponding datetime object.
    :param orig_time: Formatted string containing a date and time from a local timezone
    :return: A datetime object corresponding to the input string in UTC
    """
    try:
        # Truncating the string to contain only required values and removing unwanted whitespace
        trunc_date = orig_time[:31] if len(orig_time) > 31 else orig_time
        trunc_date = trunc_date.strip()
        if "GMT" in trunc_date:
            trunc_date = trunc_date.replace("GMT", "+0000")
        elif "PST" in trunc_date:
            trunc_date = trunc_date.replace("PST", "-0800")
        elif "EST" in trunc_date:
            trunc_date = trunc_date.replace("EST", "-0500")
        elif "EET" in trunc_date:
            trunc_date = trunc_date.replace("EET", "+0200")
        elif "CET" in trunc_date:
            trunc_date = trunc_date.replace("CET", "+0100")

        # Generating a datetime object considering multiple formats of the input parameter - with and without weekday
        if len(trunc_date) > 30 and trunc_date[14] == ':':
            datetime_obj = datetime.datetime.strptime(trunc_date, "%a, %b %d %H:%M:%S %Y %z")
        elif len(trunc_date) == 25 or len(trunc_date) == 26:
            datetime_obj = datetime.datetime.strptime(trunc_date, "%d %b %Y %H:%M:%S %z")
        elif trunc_date[3] == ',' and (len(trunc_date) == 28 or len(trunc_date) == 29) and '+' not in trunc_date and '-' not in trunc_date:
            datetime_obj = datetime.datetime.strptime(trunc_date, "%a, %d %b %Y %H:%M:%S %Z")
        elif len(trunc_date) == 27 or len(trunc_date) == 28:
            datetime_obj = datetime.datetime.strptime(trunc_date, "%a, %d %b %Y %H:%M %z")
        elif str.isalpha(trunc_date[5]) and str.isdigit(trunc_date[-1]):
            datetime_obj = datetime.datetime.strptime(trunc_date, "%a, %b %d %H:%M:%S %z %Y")
        else:
            datetime_obj = datetime.datetime.strptime(trunc_date, "%a, %d %b %Y %H:%M:%S %z")

        # Converting the datetime object into a formatted string
        utc_dt = datetime_obj.astimezone(pytz.utc)
        return utc_dt

    except:
        print("Unable to process date:", orig_time, trunc_date)
        traceback.print_exc()


def get_utc_time(orig_time):
    """
    A function to convert a formatted string containing date and time from a local timezone to UTC, by taking into
    consideration multiple formats of the input parameter
    :param orig_time: Formatted string containing a date and time from a local timezone
    :return: Formatted string containing the date and time in UTC
    """
    orig_time = str(orig_time)
    try:
        # Truncating the string to contain only required values and removing unwanted whitespace
        trunc_date = orig_time[:31] if len(orig_time) > 31 else orig_time
        trunc_date = trunc_date.strip()
        if "GMT" in trunc_date:
            trunc_date = trunc_date.replace("GMT", "+0000")
        elif "PST" in trunc_date:
            trunc_date = trunc_date.replace("PST", "-0800")
        elif "PDT" in trunc_date:
            trunc_date = trunc_date.replace("PDT", "-0800")
        elif "EST" in trunc_date:
            trunc_date = trunc_date.replace("EST", "-0500")
        elif "EET" in trunc_date:
            trunc_date = trunc_date.replace("EET", "+0200")
        elif "CET" in trunc_date:
            trunc_date = trunc_date.replace("CET", "+0100")
        # Generating a datetime object considering multiple formats of the input parameter - with and without weekday

        if len(trunc_date) > 30 and trunc_date[14] == ':':
            datetime_obj = datetime.datetime.strptime(trunc_date, "%a, %b %d %H:%M:%S %Y %z")
        elif len(trunc_date) == 25 or len(trunc_date) == 26:
            datetime_obj = datetime.datetime.strptime(trunc_date, "%d %b %Y %H:%M:%S %z")
        elif trunc_date[3] == ',' and (len(trunc_date) == 28 or len(trunc_date) == 29) and '+' not in trunc_date and '-' not in trunc_date:
            datetime_obj = datetime.datetime.strptime(trunc_date, "%a, %d %b %Y %H:%M:%S %Z")
        elif len(trunc_date) == 27 or len(trunc_date) == 28:
            datetime_obj = datetime.datetime.strptime(trunc_date, "%a, %d %b %Y %H:%M %z")
        elif str.isalpha(trunc_date[5]) and str.isdigit(trunc_date[-1]):
            datetime_obj = datetime.datetime.strptime(trunc_date, "%a, %b %d %H:%M:%S %z %Y")
        else:
            datetime_obj = datetime.datetime.strptime(trunc_date, "%a, %d %b %Y %H:%M:%S %z")

        # Converting the datetime object into a formatted string
        utc_dt = datetime_obj.astimezone(pytz.utc)
        return utc_dt.strftime("%a, %d %b %Y %H:%M:%S %z")

    except:
        # print("Unable to process date:", orig_time, trunc_date)
        return "Error"


def get_messages_before(time_limit, nodelist_filename):
    """
    This function returns a set of Message-IDs that have arrived before the time limit passed as parameter.
    :param time_limit: A string formatted time stamp in one of the recognized formats.
    :return: A set containing Message-IDs that have arrived before the time limit passed as parameter.
    """
    time_limit = get_datetime_object(time_limit)
    msgs_before_time = set()
    with open(nodelist_filename, "r") as node_file:
        for pair in node_file:
            node = pair.split(';', 2)
            sent_time = node[2].strip()
            if get_datetime_object(sent_time) < time_limit:
                msgs_before_time.add(int(node[0]))
        node_file.close()
    return msgs_before_time
def add_elements_to_graph(ignore_lat, nodelist_filename, time_limit, msgs_before_time, email_re, edgelist_filename,
                          discussion_graph):
    # Add nodes into NetworkX graph by reading from CSV file
    if not ignore_lat:
        with open(nodelist_filename, "r") as node_file:
            for pair in node_file:
                node = pair.split(';')
                if get_datetime_object(node[2].strip()) < time_limit:
                    node[0] = int(node[0])
                    msgs_before_time.add(node[0])
                    from_addr = email_re.search(node[1].strip())
                    from_addr = from_addr.group(0) if from_addr is not None else node[1].strip()
                    discussion_graph.add_node(node[0], time=node[2].strip(), color="#ffffff", style='bold',
                                              sender=from_addr)
            node_file.close()
        print("Nodes added.")

        # Add edges into NetworkX graph by reading from CSV file
        with open(edgelist_filename, "r") as edge_file:
            for pair in edge_file:
                edge = pair.split(';')
                edge[0] = int(edge[0])
                edge[1] = int(edge[1])
                if edge[0] in msgs_before_time and edge[1] in msgs_before_time:
                    discussion_graph.add_edge(*edge)
            edge_file.close()
        print("Edges added.")

    else:
        lone_author_threads = get_lone_author_threads(save_file=None, nodelist_filename=nodelist_filename,
                                                      edgelist_filename=edgelist_filename)
        # Add nodes into NetworkX graph only if they are not a part of a thread that has only a single author
        with open(nodelist_filename, "r") as node_file:
            for pair in node_file:
                node = pair.split(';')
                node[0] = int(node[0])
                if get_datetime_object(node[2].strip()) < time_limit and node[0] not in lone_author_threads:
                    msgs_before_time.add(node[0])
                    from_addr = email_re.search(node[1].strip())
                    from_addr = from_addr.group(0) if from_addr is not None else node[1].strip()
                    discussion_graph.add_node(node[0], time=node[2].strip(), color="#ffffff", style='bold',
                                              sender=from_addr)
            node_file.close()
        print("Nodes added.")

        if len(msgs_before_time) == 0:
            return "No messages!"

        # Add edges into NetworkX graph only if they are not a part of a thread that has only a single author
        with open(edgelist_filename, "r") as edge_file:
            for pair in edge_file:
                edge = pair.split(';')
                edge[0] = int(edge[0])
                edge[1] = int(edge[1])
                if edge[0] not in lone_author_threads and edge[1] not in lone_author_threads:
                    if edge[0] in msgs_before_time and edge[1] in msgs_before_time:
                        discussion_graph.add_edge(*edge)
            edge_file.close()
        print("Edges added.")


def load_json(ignore_lat, time_lbound, time_ubound, email_re, json_data, json_filename):
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
        print("JSON data loaded.")
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
