"""
This module is used to  graphs that show the interaction between authors in the mailing list. There is an edge from
one author to another if the former sent a message to the latter either in To or by marking in CC. These graphs are for
the entire mailing list.
"""
import json
from util.read import *


def write_to_pajek(author_graph, filename="author_graph.net"):
	"""
	
	Write the networkx graph in Pajek format to author_graph.net
	
	:param author_graph: Networkx graph.
	:param filename: Write to Pajek file compatible with the Infomap Community Detection module.
	"""
	# Write Pajek file compatible with the Infomap Community Detection module
	nx.write_pajek(author_graph, filename)
	lines_in_file= list()
	with open(filename, 'r') as pajek_file:
		for line in pajek_file:
			lines_in_file.append(line)
	num_vertices = int(lines_in_file[0].split()[1])

	for i in range(1, num_vertices+1):
		line = lines_in_file[i].split()
		line[1] = "\"" + line[1] + "\""
		del line[2:]
		line.append("\n")
		lines_in_file[i] = " ".join(line)

	with open(filename, 'w') as pajek_file:
		for line in lines_in_file:
			pajek_file.write(line)


def author_interaction():
	"""

	Prints the number of strongly connected components,weekly connected components, number of nodes and edges from the author graph.
	"""
	# Time limit can be specified here in the form of a timestamp in one of the identifiable formats and all messages
	# that have arrived after this timestamp will be ignored.
	time_limit = None
	# If true, then messages that belong to threads that have only a single author are ignored.
	ignore_lat = True
	author_graph = nx.DiGraph()
	email_re = re.compile(r'[\w\.-]+@[\w\.-]+')
	json_data = dict()
	if time_limit is None:
		time_limit = time.strftime("%a, %d %b %Y %H:%M:%S %z")
	msgs_before_time = set()
	time_limit = get_datetime_object(time_limit)
	print("All messages before", time_limit, "are being considered.")

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
		for to_address in addr_list:
			author_graph.add_edge(message['From'], to_address)

	write_to_pajek(author_graph)

	print("No. of Weakly Connected Components:", nx.number_weakly_connected_components(author_graph))
	print("No. of Strongly Connected Components:", nx.number_strongly_connected_components(author_graph))
	print("Nodes:", nx.number_of_nodes(author_graph))
	print("Edges:", nx.number_of_edges(author_graph))

