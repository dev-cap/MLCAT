from util.read import *
import json
import os.path
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt


def inv_func(x, a, b, c):
    """

    The model function used for curve fitting.
    """
    return a/x + b/(x**2) + c


def conversation_refresh_times(headers_filename, nodelist_filename, edgelist_filename, foldername, time_ubound = None, time_lbound = None, plot=False):
    """
    

    :param headers_filename: The JSON file containing the headers.
    :param nodelist_filename: The csv file containing the nodes.
    :param edgelist_filename: The csv file containing the edges.
    :param foldername: The mailbox folder.
    :param time_ubound: Time limit upper bound can be specified here in the form of a timestamp in one of the identifiable formats
            and all messages that have arrived after this timestamp will be ignored.
    :param time_lbound: Time limit lower bound can be specified here in the form of a timestamp in one of the identifiable formats
            and all messages that have arrived before this timestamp will be ignored.
    :param plot: Plot thread based time statistics if True.
    :return: None if successfully plotted, else 'No messages!'.
    """
    # Time limit can be specified here in the form of a timestamp in one of the identifiable formats. All messages
    # that have arrived after time_ubound and before time_lbound will be ignored.

    # If ignore_lat is true, then messages that belong to threads that have only a single author are ignored.
    ignore_lat = False

    discussion_graph = nx.DiGraph()
    email_re = re.compile(r'[\w\.-]+@[\w\.-]+')
    msgs_before_time = set()
    json_data = dict()

    if time_ubound is None:
        time_ubound = time.strftime("%a, %d %b %Y %H:%M:%S %z")
    time_ubound = get_datetime_object(time_ubound)

    if time_lbound is None:
        time_lbound = "Sun, 01 Jan 2001 00:00:00 +0000"
    time_lbound = get_datetime_object(time_lbound)

    print("All messages before", time_ubound, "and after", time_lbound, "are being considered.")

    # Add nodes into NetworkX graph by reading from CSV file
    if not ignore_lat:
        with open(nodelist_filename, "r") as node_file:
            for pair in node_file:
                node = pair.split(';', 2)
                if get_datetime_object(node[2].strip()) < time_ubound:
                    node[0] = int(node[0])
                    msgs_before_time.add(node[0])
                    from_addr = email_re.search(node[1].strip())
                    from_addr = from_addr.group(0) if from_addr is not None else node[1].strip()
                    discussion_graph.add_node(node[0], time=node[2].strip(), color="#ffffff", style='bold',
                                              sender=from_addr)
            node_file.close()
        print("Nodes added.")

        if len(msgs_before_time) == 0:
            return "No messages!"

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
        lone_author_threads = get_lone_author_threads(False)
        # Add nodes into NetworkX graph only if they are not a part of a thread that has only a single author
        with open(nodelist_filename, "r") as node_file:
            for pair in node_file:
                node = pair.split(';', 2)
                node[0] = int(node[0])
                if get_datetime_object(node[2].strip()) < time_ubound and node[0] not in lone_author_threads:
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

    if not ignore_lat:
        with open(headers_filename, 'r') as json_file:
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
        with open(headers_filename, 'r') as json_file:
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

    # The list crt stores the conversation refresh times between authors as a list of tuples containing the author
    # email IDs and the time in seconds.
    crt = list()

    # The last_conv_time dictionary stores the timestamp of the authors' last conversation. The items in the dictionary
    # are referenced by a set containing the authors' email IDs.
    last_conv_time = dict()

    for msg_id, message in sorted(json_data.items(), key = lambda x1: x1[1]['Time']):
        if message['Cc'] is None:
            addr_list = message['To']
        else:
            addr_list = message['To'] | message['Cc']

        for to_address in addr_list:
            if to_address > message['From']:
                addr1 = message['From']
                addr2 = to_address
            else:
                addr2 = message['From']
                addr1 = to_address

            if last_conv_time.get((addr1, addr2), None) is None:
                last_conv_time[(addr1, addr2)] = (message['Message-ID'], message['Time'])
            elif not nx.has_path(discussion_graph, message['Message-ID'], last_conv_time[(addr1, addr2)][0])\
                    and not nx.has_path(discussion_graph, last_conv_time[(addr1, addr2)][0], message['Message-ID']):
                crt.append((message['From'], to_address,
                            (message['Time']-last_conv_time[((addr1, addr2))][1]).total_seconds()))
                last_conv_time[(addr1, addr2)] = (message['Message-ID'], message['Time'])

    if len(crt) != 0:
        if not os.path.exists(foldername):
            os.makedirs(foldername)

        with open(foldername + "/conversation_refresh_times.csv", mode='w') as dist_file:
            dist_file.write("From Address;To Address;Conv. Refresh Time\n")
            for from_addr, to_address, crtime in crt:
                if crtime > 9:
                    dist_file.write("{0};{1};{2}\n".format(from_addr, to_address, str(crtime)))
            dist_file.close()

        if plot:
            crt = sorted([z for x, y, z in crt if z > 9])[:int(.9*len(crt))]
            y, x1 = np.histogram(crt, bins=50)
            y = list(y)
            max_y = sum(y)
            if max_y != 0:
                y = [y1 / max_y for y1 in y]
            x = list()
            for i1 in range(len(x1)-1):
                x.append((x1[i1]+x1[i1+1])/2)
            popt, pcov = curve_fit(inv_func, x, y)
            a, b, c = popt
            plt.figure()
            axes = plt.gca()
            axes.set_xlim([0, max(x)])
            axes.set_ylim([0, max(y)])
            plt.plot(x, y, linestyle='--', color='b', label="Data")
            plt.savefig(foldername + '/conversation_refresh_times.png')
            x_range = np.linspace(min(x), max(x), 500)
            plt.plot(x_range, a/x_range + b/(x_range**2) + c, 'r-', label="Fitted Curve")
            plt.legend()
            plt.savefig(foldername + '/conversation_refresh_times_inv.png')
            plt.close()
        return None

    else:
        return "No messages!"




