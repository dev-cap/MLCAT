"""
This module is used to generate bipartite graph among all the users and messages in the mailing list such that all
the users are on one side and all the messages will be on another. A directed edge would be drawn from author to the
message sent by the author. A directed edge would be drawn from message to all the users who are in To and CC fields.
A projection of this bipartite graph is then generated.
"""
import json
from util.read import *


def msg_author_bipartite_graph(threadwise=False, ignore_lat=True, time_limit=None):
    """

    :param threadwise: If true, a bipartite graph is generated for each thread individually.
    :param ignore_lat: If true, then messages that belong to threads that have only a single author are ignored.
    :param time_limit: Time limit can be specified here in the form of a timestamp in one of the identifiable formats
            and all messages that have arrived after this timestamp will be ignored.
    """
    email_re = re.compile(r'[\w\.-]+@[\w\.-]+')
    json_data = dict()
    if time_limit is None:
        time_limit = time.strftime("%a, %d %b %Y %H:%M:%S %z")
    msgs_before_time = set()
    time_limit = get_datetime_object(time_limit)
    print("All messages before", time_limit, "are being considered.")

    if threadwise:
        # Generate a bipartite graph for each thread individually
        discussion_graph = nx.DiGraph()
        # Add nodes into NetworkX graph by reading from CSV file
        if not ignore_lat:
            with open("graph_nodes.csv", "r") as node_file:
                for pair in node_file:
                    node = pair.split(';', 2)
                    if get_datetime_object(node[2].strip()) < time_limit:
                        node[0] = int(node[0])
                        msgs_before_time.add(node[0])
                        from_addr = email_re.search(node[1].strip())
                        from_addr = from_addr.group(0) if from_addr is not None else node[1].strip()
                        discussion_graph.add_node(node[0], time=node[2].strip(), sender=from_addr)
                node_file.close()
            print("Nodes added.")
            # Add edges into NetworkX graph by reading from CSV file
            with open("graph_edges.csv", "r") as edge_file:
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
            with open("graph_nodes.csv", "r") as node_file:
                for pair in node_file:
                    node = pair.split(';', 2)
                    node[0] = int(node[0])
                    if get_datetime_object(node[2].strip()) < time_limit and node[0] not in lone_author_threads:
                        msgs_before_time.add(node[0])
                        from_addr = email_re.search(node[1].strip())
                        from_addr = from_addr.group(0) if from_addr is not None else node[1].strip()
                        discussion_graph.add_node(node[0], time=node[2].strip(), color="#ffffff", style='bold', sender=from_addr)
                node_file.close()
            print("Nodes added.")
            # Add edges into NetworkX graph only if they are not a part of a thread that has only a single author
            with open("graph_edges.csv", "r") as edge_file:
                for pair in edge_file:
                    edge = pair.split(';')
                    edge[0] = int(edge[0])
                    edge[1] = int(edge[1])
                    if edge[0] not in lone_author_threads and edge[1] not in lone_author_threads:
                        if edge[0] in msgs_before_time and edge[1] in msgs_before_time:
                            discussion_graph.add_edge(*edge)
                edge_file.close()
            print("Edges added.")

        with open('clean_data.json', 'r') as json_file:
            for chunk in lines_per_n(json_file, 9):
                json_obj = json.loads(chunk)
                json_obj['Message-ID'] = int(json_obj['Message-ID'])
                json_obj['Time'] = datetime.datetime.strptime(json_obj['Time'], "%a, %d %b %Y %H:%M:%S %z")
                # print("\nFrom", json_obj['From'], "\nTo", json_obj['To'], "\nCc", json_obj['Cc'])
                from_addr = email_re.search(json_obj['From'])
                json_obj['From'] = from_addr.group(0) if from_addr is not None else json_obj['From']
                json_obj['To'] = set(email_re.findall(json_obj['To']))
                json_obj['Cc'] = set(email_re.findall(json_obj['Cc'])) if json_obj['Cc'] is not None else None
                # print("\nFrom", json_obj['From'], "\nTo", json_obj['To'], "\nCc", json_obj['Cc'])
                json_data[json_obj['Message-ID']] = json_obj
        print("JSON data loaded.")

        for conn_subgraph in nx.weakly_connected_component_subgraphs(discussion_graph):
            bipartite_graph = nx.DiGraph()
            for node_uid in conn_subgraph.nodes():
                message = json_data[node_uid]
                if message['Cc'] is None:
                    addr_list = message['To']
                else:
                    addr_list = message['To'] | message['Cc']
                bipartite_graph.add_edge(message['From'], message['Message-ID'], style='solid')
                for to_address in addr_list:
                    bipartite_graph.add_edge(message['Message-ID'], to_address, style='dashed')
                # Do something!
                print("No. of Nodes: ", nx.number_of_nodes(bipartite_graph))
                print("No. of Edges: ", nx.number_of_edges(bipartite_graph))
    else:
        # Make a message author bipartite graph for all the threads
        bipartite_graph = nx.DiGraph()
        if not ignore_lat:
            with open('clean_data.json', 'r') as json_file:
                for chunk in lines_per_n(json_file, 9):
                    json_obj = json.loads(chunk)
                    json_obj['Message-ID'] = int(json_obj['Message-ID'])
                    json_obj['Time'] = datetime.datetime.strptime(json_obj['Time'], "%a, %d %b %Y %H:%M:%S %z")
                    if json_obj['Time'] < time_limit:
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
            with open('clean_data.json', 'r') as json_file:
                for chunk in lines_per_n(json_file, 9):
                    json_obj = json.loads(chunk)
                    json_obj['Message-ID'] = int(json_obj['Message-ID'])
                    if json_obj['Message-ID'] not in lone_author_threads:
                        json_obj['Time'] = datetime.datetime.strptime(json_obj['Time'], "%a, %d %b %Y %H:%M:%S %z")
                        if json_obj['Time'] < time_limit:
                            # print("\nFrom", json_obj['From'], "\nTo", json_obj['To'], "\nCc", json_obj['Cc'])
                            from_addr = email_re.search(json_obj['From'])
                            json_obj['From'] = from_addr.group(0) if from_addr is not None else json_obj['From']
                            json_obj['To'] = set(email_re.findall(json_obj['To']))
                            json_obj['Cc'] = set(email_re.findall(json_obj['Cc'])) if json_obj['Cc'] is not None else None
                            # print("\nFrom", json_obj['From'], "\nTo", json_obj['To'], "\nCc", json_obj['Cc'])
                            json_data[json_obj['Message-ID']] = json_obj
            print("JSON data loaded.")

        for msg_id, message in json_data.items():
            if message['Cc'] is None:
                addr_list = message['To']
            else:
                addr_list = message['To'] | message['Cc']
            bipartite_graph.add_edge(message['From'], message['Message-ID'], style='solid')
            for to_address in addr_list:
                bipartite_graph.add_edge(message['Message-ID'], to_address, style='dashed')

        print("No. of Nodes: ", nx.number_of_nodes(bipartite_graph))
        print("No. of Edges: ", nx.number_of_edges(bipartite_graph))
        print("No. of Weakly Connected Components: ", nx.number_weakly_connected_components(bipartite_graph))
        print("No. of Strongly Connected Components: ", nx.number_strongly_connected_components(bipartite_graph))
        # Do something!
