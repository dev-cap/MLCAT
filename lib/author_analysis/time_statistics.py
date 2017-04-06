from util.read_utils import *
import json
import os.path
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt


def inv_func(x, a, b, c):
    return a / x + b / (x ** 2) + c


def conversation_refresh_times(headers_filename, nodelist_filename, edgelist_filename, foldername, time_ubound=None,
                               time_lbound=None, plot=False):
    """

    :param json_data:
    :param discussion_graph:
    :return:
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
    # Added a new variable time_limit to match other modules for refactoring purpose
    time_limit = time_ubound
    # Call this new function in read_utils.py
    add_elements_to_graph(ignore_lat, nodelist_filename, time_limit, msgs_before_time, email_re, edgelist_filename,
                          discussion_graph)

    # call the new function from read_utils.py
    load_json(ignore_lat, time_lbound, time_ubound, email_re, json_data, json_filename=headers_filename)

    # The list crt stores the conversation refresh times between authors as a list of tuples containing the author
    # email IDs and the time in seconds.
    crt = list()

    # The last_conv_time dictionary stores the timestamp of the authors' last conversation. The items in the dictionary
    # are referenced by a set containing the authors' email IDs.
    last_conv_time = dict()

    for msg_id, message in sorted(json_data.items(), key=lambda x1: x1[1]['Time']):
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
            elif not nx.has_path(discussion_graph, message['Message-ID'], last_conv_time[(addr1, addr2)][0]) \
                    and not nx.has_path(discussion_graph, last_conv_time[(addr1, addr2)][0], message['Message-ID']):
                crt.append((message['From'], to_address,
                            (message['Time'] - last_conv_time[((addr1, addr2))][1]).total_seconds()))
                last_conv_time[(addr1, addr2)] = (message['Message-ID'], message['Time'])

    if len(crt) != 0:
        if not os.path.exists(foldername):
            os.makedirs(foldername)

        with open(foldername + "conversation_refresh_times.csv", mode='w') as dist_file:
            dist_file.write("From Address;To Address;Conv. Refresh Time\n")
            for from_addr, to_address, crtime in crt:
                if crtime > 9:
                    dist_file.write("{0};{1};{2}\n".format(from_addr, to_address, str(crtime)))
            dist_file.close()

        if plot:
            crt = sorted([z for x, y, z in crt if z > 9])[:int(.9 * len(crt))]
            y, x1 = np.histogram(crt, bins=50)
            y = list(y)
            max_y = sum(y)
            if max_y != 0:
                y = [y1 / max_y for y1 in y]
            x = list()
            for i1 in range(len(x1) - 1):
                x.append((x1[i1] + x1[i1 + 1]) / 2)
            popt, pcov = curve_fit(inv_func, x, y)
            a, b, c = popt
            plt.figure()
            axes = plt.gca()
            axes.set_xlim([0, max(x)])
            axes.set_ylim([0, max(y)])
            plt.plot(x, y, linestyle='--', color='b', label="Data")
            plt.savefig(foldername + 'conversation_refresh_times.png')
            x_range = np.linspace(min(x), max(x), 500)
            plt.plot(x_range, a / x_range + b / (x_range ** 2) + c, 'r-', label="Fitted Curve")
            plt.legend()
            plt.savefig(foldername + 'conversation_refresh_times_inv.png')
            plt.close()
        return None

    else:
        return "No messages!"


