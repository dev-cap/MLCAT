"""
This module is used to  graphs that show the interaction between authors in the mailing list. There is an edge from
one author to another if the former sent a message to the latter either in To or by marking in CC. These graphs are for
the entire mailing list.
"""
import json
from util.read import *


def generate_edge_list(author_nodelist_filename, author_edgelist_filename, nodelist_filename='graph_nodes.csv',
					   edgelist_filename='graph_edges.csv', threads_json_filename='clean_data.json', author_json_filename='author_uid_map.json'):
	"""
	
	:param author_nodelist_filename: The csv file containing the author nodes data.
	:param author_edgelist_filename: The csv file containing the author edges data.
	:param nodelist_filename: The csv file containing the nodes.
	:param edgelist_filename: The csv file containing the edges.
	:param threads_json_filename: The JSON file containing the cleaned headers.
	:param author_json_filename: The JSON file containing the author UID map.
	"""
	# Time limit can be specified here in the form of a timestamp in one of the identifiable formats and all messages
	# that have arrived after this timestamp will be ignored.
	# If true, then messages that belong to threads that have only a single author are ignored.
	time_limit = None
	ignore_lat = True
	author_graph = nx.DiGraph()
	with open(author_json_filename, 'r') as author_uid_file:
		author_uid_map = json.load(author_uid_file)
	email_re = re.compile(r'[\w\.-]+@[\w\.-]+')
	json_data = dict()
	if time_limit is None:
		time_limit = time.strftime("%a, %d %b %Y %H:%M:%S %z")
	msgs_before_time = set()
	time_limit = get_datetime_object(time_limit)
	print("All messages before", time_limit, "are being considered.")

	if not ignore_lat:
		with open(threads_json_filename, 'r') as json_file:
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
		lone_author_threads = get_lone_author_threads(None, nodelist_filename, edgelist_filename)
		with open(threads_json_filename, 'r') as json_file:
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
		for to_address in addr_list:
			author_graph.add_edge(author_uid_map[message['From']], author_uid_map[to_address])

	nx.write_edgelist(author_graph, author_edgelist_filename, delimiter="\t")

	with open(author_nodelist_filename, 'w') as nodelist_file:
		for author_address, author_uid in author_uid_map.items():
			nodelist_file.write(str(author_uid) + "\t" + author_address + "\n")

	# print("No. of Weakly Connected Components:", nx.number_weakly_connected_components(author_graph))
	# print("No. of Strongly Connected Components:", nx.number_strongly_connected_components(author_graph))
	# print("Nodes:", nx.number_of_nodes(author_graph))
	# print("Edges:", nx.number_of_edges(author_graph))

# generate_edge_list(author_nodelist_filename='./data/lkml/tables/author_graph_nodes.txt', author_edgelist_filename='./data/lkml/tables/author_graph_edges.txt',
#                    nodelist_filename='./data/lkml/tables/graph_nodes.csv', edgelist_filename='./data/lkml/tables/graph_edges.csv',
#                    threads_json_filename="./data/lkml/json/clean_data.json", author_json_filename='./data/lkml/json/author_uid_map.json')


