Overview of Project Modules
###########################

imap\_conn.py
=============

This file contains a function to establish connection to the IMAP server
of Gmail, in order to access the inbox of the mail account subscribed to
the Linux kernel mailing list. A point to be noted is that the IMAP
service must be enabled in the account in order to obtain connection to
the said account. The open\_connection() function is used to open a SSL
connection to the IMAP mail server. A configuration file contains
details of the server hostname, username and password required to login
to the mail account. This functions reads all such details from the
configuration file and uses it to open a connection. It then returns the
connection object thus created.

encoder.py
==========

This file contains two classes, namely – NoIndent and MyEncoder. These
classes override the default encoder of the json module. They are used
for pretty printing of lists in the JSON objects onto the JSON files.
The purpose of the NoIndent class is to convert the value of its object
(if it is a list) to a string of comma separated elements of the list.
This is defined in its **repr**\ () method. The MyEncoder class inherits
the JSONEncoder class defined in the JSON module. It overrides the
default() method. This method is used when writing JSON objects on to a
file. It uses the default representation as present in the default()
method as present in the parent class for objects of all types except
those of type NoIndent. In case a NoIndent object is passed, then it
uses the representation as specified in the **repr**\ () method in the
NoIndent class.

imap\_hdr.py
============

This module contains the parser component required to extract
information from mail headers. The function that aids with this task is
**get\_mail\_header()** which fetches the emails from the IMAP server as
per the parameters passed. The parameters can either be a list or a
range of UIDs. The parser uses the connection object returned by the
open\_connection() function present in the imap\_conn.py file. The
returned object is used to select the ‘INBOX’ folder of the mail
account, after which a search for all mails in the inbox satisfying a
given criteria specified in terms of the Message-UID. The UID is a
unique number that the mail client associates with each mail. From the
header obtained, we extract the required information specified before
and write it onto a JSON file.

Since the Message-ID and the list of references obtained from each
header is a tokenizable string which are difficult to handle for any
sort of numerical analysis, each Message-ID is associated with a unique
number and this mapping is written into the uid\_map.json file.
Information on the headers of all mails sent in the time period before
the subscription to the mailing list would not be made available and in
such a case, a value of 0 is mapped to the message-id string. The
references list is then packaged in a NoIndent object so that, while
writing the references field into the JSON file, the **repr**\ () method
of the NoIndent class  result in a representation of the list contained within a line to help with the pretty printing. All of the header details are stored in the headers.json file.

The **init_uid_map()** function ensures that references are correctly recorded in the JSON file such that there are no references to mails that do not exist and to ease the processing of headers by initializing a map with the string in the Message-Id field of the header to the UID of the mail. This function reads the header.json file and adds required entries to the map before the process of fetching new headers. The **date_to_UTC()** function converts a formatted string containing date and time from a local timezone to UTC, by taking into consideration the multiple possible formats of the input parameter.

mbox\_hdr.py
============

This module is analogous to the “imap\_hdr.py” module. From the .MBOX
file, the header information is extracted using two predefined classes
available in the Python Standard Library: Mailbox and Message, for
accessing and manipulating on-disk mailboxes and the messages they
contain respectively. Mailbox offers a dictionary-like mapping from keys
to message and messages can be a string or a file and that contain an
RFC 2822-compliant message, which is read and parsed. The messages are
parsed and the header information containing the fields From, To, CC,
Message-ID, In-Reply-To, Reference and Time is extracted for each
message in the .MBOX file and is then saved to a JSON file
(“headers.json”). The Reference and In-Reply-To fields are used to
reconstruct the thread and they point to either a Message\_ID or to 0
(referring to a mail not present in the mailbox file). Hence an unique
Message-ID is provided to each message in the .MBOX file in the
ascending order of their arrival times. The The mapping between the UIDs
and Message-IDs are stored in another JSON file
(“thread\_uid\_map.json”) in order to facilitate the reconstruction of
the threads. The formatting of the JSON file is identical to the one
provided by the “imap\_hdr.py” module.

imap\_fetch\_headers.py
=======================

This is the driver module to fetch mail headers from the IMAP server.
Here, the range of Message IDs to be fetched can be specified and the
JSON file is then cleaned to remove such orphaned children nodes using
the “data\_cleanup.py” module and saved to clean\_data.json after
removal of duplicate, unwanted and invalid entries in the headers.json
file using the “check\_headers.py” module.

mbox\_fetch\_headers.py
=======================

This module is analogous to the “imap\_fetch\_headers.py” module. This
is the driver module to fetch mail headers from an MBOX file. After the
removal of duplicate, unwanted and invalid entries in the headers.json
file using the “check\_headers.py” module, the JSON file thus generated
is then cleaned to remove orphaned children nodes using the
“data\_cleanup.py” module and saved to clean\_data.json in a process
that is similar to the one used for headers fetched directly from the
IMAP servers.

data\_cleanup.py
================

Since we have access to the mails after the time of subscription to the
mailing list, if any of the mails contain a reference to mails before
subscription (in the form of a 0 in its list of references), then their
references field is incomplete and cannot be included for analysis.
Hence, the data present in headers.json file must be cleaned before
proceeding further. This is done by the
**remove\_invalid\_references()** function in this module. Here, one
JSON object at a time is read from the headers.json file using the
**lines\_per\_n()** function from the **read\_json** module under the
**util** package, which takes as arguments the file object and the
number of lines to be read and combined into a single string.The string
returned thus is used by the json.loads() function to load the JSON
object.

For each JSON object obtained as mentioned above, the presence of a
0-reference is checked for. The Message-IDs of all such mails are added
to a set and the object are then discarded. Even if JSON objects that do
not have a 0 in its list of references have a reference to any of the
Messaged-IDs that are present in the above set they are discarded. The
headers that are not incomplete are then written into another JSON file
(clean\_data.json). Note that if the list of references of the of the
mail is None, then such mails are indicative of being the root of a
thread of discussion and such headers are valid and complete.

check\_headers.py
=================

This module contains all the necessary functions for the maintenance of
the JSON file such as: \* get\_unavailable\_uid(): This function returns
a list of UIDs which are not available in the IMAP server and hence
can’t be fetched by imap\_hdr() \* check\_validity(): This function
checks for and prints duplicate, missing, and invalid objects in the
“headers.json” file. This function can be run first to generate a list
of duplicate, missing, or invalid objects’ UIDs which can then be used
to add or remove their entries from the JSON file. \*
remove\_unwanted\_headers(): This function removes all the UIDs
specified in the to\_remove parameter. By default, it removes all the
unwanted entries in the JSON file, i.e. the list of UIDs of mails that
are not forwarded from LKML subscription. \*
remove\_duplicate\_headers(): This function removes the duplicate
entries of the UIDs specified in the to\_remove parameter, such that
each UID has only an unique entry. By default, it removes all the
duplicate entries in the JSON file. \* add\_missing\_headers(): This
function adds the mails that have been missed out, considering the fact
that UIDs are consecutive. If a mail that is missing in the JSON file is
not available or has been deleted, this function ignores that UID. \*
replace\_invalid\_headers(): This function removes the mail headers that
have insufficient attributes and fetches those headers again. If an
attribute is missing in the original mail header or if the mail has been
deleted, this function ignores that UID.

-  write\_uid\_map(): To ensure that references are correctly recorded
   in the JSON file such that there are no references to mails that do
   not exist and to ease the processing of headers, a map with the
   string in the Message-Id field of the header to the UID of the mail
   is required. This function fetches the headers from the IMAP server
   and adds the required pairs of Message\_ID and UID to the JSON file.

graph\_edges.py
===============

This module reads from clean\_data.json and writes a list of all nodes
and edges into a separate CSV file. To make the graph\_edges.csv file,
for every mail in a thread the last Message-ID in the list of references
indicates the message-id of the immediate ancestor or parent of the mail
in the thread. Wherever the list is present, the last element is
extracted from it and is written onto the file along with the Message-ID
of the current thread in the following format: * ;< message-id>*.
Similarly for graph\_nodes.csv, the Message\_ID, the sender’s mail
address and the time-stamp is written into as comma separated values.
Both the edge list and the node list are used to generate graphs and
width height tables.

graph\_generate\_threads.py
===========================

This module is used to generate a thread-wise view of the entire mailing
list by saving the a graph representing the messages in a thread as a
tree using the References and In-Reply-TO fields from the mail headers.
The thread graphs are then saved to GEXF, DOT and PNG formats. All
authors of a thread are identified and each author is given a unique
colour. All messages sent by this author get the same colour. Each
messaging thread is a directed tree with directed edge going from child
mail to parent mail. If a mail elicits two responses these two child
nodes are shown at the same level.

graph\_generate\_authors.py
===========================

This module is used to graphs that show the interaction between authors
in the mailing list. There is an edge from one author to another if the
former sent a message to the latter either in To or by marking in CC.
These graphs are for the entire mailing list.

graph\_msg\_author\_bipartite.py
================================

This module is used to generate bipartite graph among all the users and
messages in the mailing list such that all the users are on one side and
all the messages will be on another. A directed edge would be drawn from
author to the message sent by the author. A directed edge would be drawn
from message to all the users who are in To and CC fields. A projection
of this bipartite graph is then generated.

graph\_thread\_author\_interaction.py
=====================================

This module is used to generate graphs that show the interaction between
authors either through multiple edges or through edge weights. There is
an edge from one author to another if the former sent a message to the
latter. These graphs depict thread-wise interaction of the authors for
the entire mailing list and these interactions are labelled in
chronological order to help identify the flow of messages across
authors.

graph\_authors\_community.py
============================

This module is used to find the community structure of the network
according to the Infomap method of Martin Rosvall and Carl T. Bergstrom
and returns an appropriate VertexClustering object. This module has been
implemented using both the iGraph package and the Infomap tool from
MapEquation.org. The VertexClustering object represents the clustering
of the vertex set of a graph and also provides some methods for getting
the subgraph corresponding to a cluster and such.

graph\_authors\_motif.py
========================

This module uses Graph-Tool.clustering package to count the occurrence
of motifs (which are k-size node-induced subgraphs) and consequently
obtain the motif significance profile, for subgraphs with k vertices.
The functions in Graph-Tool implement the ESU and RAND-ESU algorithms as
described in S. Wernicke, “Efficient detection of network motifs”,
IEEE/ACM Transactions on Computational Biology and Bioinformatics. Then
tuples with three lists are written to a text file: the list of motifs
found, the list with their respective counts, and their respective
z-scores.

hypergraph\_generate\_edge.py
=============================

This module is used to model each discussion thread as one hypergraph.
All the email header information can be represented as one hyperedge of
a hypergraph. This concise format for representing a discussion thread
as a hypergraph is then stored as a table to a CSV file, with the author
column headers containing the ids of the authors. All the author columns
are sorted left to right in the descending order of out degree, followed
by in degree. The authors identified in this discussion thread are
indexed in a separate file using the author\_uid\_map.py.

wh\_table\_threads.py
=====================

This module is used to generate the thread width height table, which is
a representation of the number of nodes in the graph that have a given
height and a given number of children in a tabular form. This table
provides an aggregate statistical view of all the discussion threads.
The table, which itself is temporarily stored in a two dimensional
array, is then written into a CSV file.

wh\_table\_authors.py
=====================

This module is used to generate the author version of the width height
table. The width height table for the authors is a representation of the
number of total and new authors in a thread aggregated at a given
generation. The table, which itself is temporarily stored in a two
dimensional array, is then written into a CSV file. These tables are can
be used to decipher the basic conversation structure. Especially, how
many 2-way, 3-way, 4-way etc. conversations happen in a discussion
thread.

participant size\_table.py
==========================

This module is used to generate a table containing the number of mails
in a thread and the corresponding aggregate count of the number of
threads that have that number of mails in them, along with the total
number of authors who have participated in such threads and the average
number of authors. This table is then written to a CSV file.

time\_statistics\_threads.py
============================

Using the headers of the messages of the threads, this module is used
for generating the following statistics can be helpful in understanding
the nature of the discussion threads: \* *Distribution of the length*
(in units of time) of each discussion thread. Since one discussion
thread has one length, we have a distribution of these lengths. \*
*Distribution of inter-arrival times between the consecutive messages*
in all discussion threads. This information would help in determining a
possible termination of a discussion thread. If there is no activity on
a thread beyond a reasonable limit (can be mean + 2\*S.D), then we can
conclude the discussion thread to be dead. Both these distributions can
then be plotted as cumulative distribution functions (CDFs) using the
CSV files generated by this module.

author\_uid\_map.py
===================

This module is used to generate and write to a JSON file the mapping of
authors to a unique integer identifier. Authors are identified through a
regular expression search for their email addresses. The integer
identifiers generated are used in other modules like the generation and
statistical analysis of hyperedges.

read\_utils.py
==============

This module contains functions that help in parsing the JSON files
containing the mail headers such as: \* lines\_per\_n(): Each JSON
object in the headers.json file occupies a set number of lines. This
function is used to read those set number of lines and return them. \*
get\_lone\_author\_threads(): This function returns the UID of all the
nodes that belong to a thread that has only one author. \*
get\_datetime\_object(): A function to convert a formatted string
containing date and time from a local timezone to UTC, by taking into
consideration multiple formats of the input parameter and then return
the corresponding datetime object. \* get\_utc\_time(): A function to
convert a formatted string containing date and time from a local
timezone to UTC, by taking into consideration multiple formats of the
input parameter. \* get\_messages\_before(): This function returns a set
of Message-IDs that have arrived before the time limit passed as
parameter.



