from itertools import islice, chain
import json


def lines_per_n(f, n) :

    for line in f :
        yield ''.join(chain([line], islice(f, n-1)))


with open('clean_data.json', 'r') as fil :

    for chunk in lines_per_n(fil, 9) :

        jfile = json.loads(chunk)

        msg_id = jfile['Message-ID']

        if jfile['References'] :

            ref_list = str(jfile['References']).split(',')

            # Message Id of the parent mail is appended to the end of the list of references.
            parent_id = int(ref_list[-1])

            with open('gephi_edge.csv', 'a') as csv_file :
                csv_file.write("{0};{1}\n".format(parent_id, msg_id))
                csv_file.close()