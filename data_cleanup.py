from itertools import islice, chain
import json

"""
    Each json object in the headers.json file occupies a set number of lines.
    This fuction is used to read those set number of lines and return them.
"""
def lines_per_n(f, n) :

    for line in f :
        yield ''.join(chain([line], islice(f, n-1)))

# This list is used to keep track of all those mails that have '0' in their reference list.
# This is done so that if any mail has any of the element in this list, in its list of references, we can eliminate them as well
unspecified_ref = ['0']

with open('headers.json', 'r')  as fil :

    for chunk in lines_per_n(fil, 8) :

        # jfile is used to store the json object read from the file.
        jfile = json.loads(chunk)

        """
            Mails that have references that are of type None indicate that they maybe the start of threads.
            Anything else coud be mail in a thread or something else.
        """
        if not(jfile['References'] == None) :

            # Checking if the refernces is an empty string
            if not(jfile['References'] == "") :

                #Since the refernces are stored as a comma seprated string, to convert to a list, we have to split it at the ',' to get a list.
                ref_list = jfile['References'].split(',')

                # a '0' in the list indicates that the mail contains references to some other mail which is not available to us
                if not('0' in ref_list) :

                    data = {}

                    data['Message-ID'] = jfile['Message-ID']
                    data['From'] = str(jfile['From'])
                    data['To'] = str(jfile['To'])
                    data['Cc'] = str(jfile['Cc'])
                    data['In-Reply-To'] = str(jfile['In-Reply-To'])
                    data['References'] = str(jfile['References'])   

                    contain_unspec_ref = False

                    # This is done to eleminate all those mails whose reference list contains mails that have '0' in their reference list
                    for ref in ref_list :
                        if ref in unspecified_ref :
                            contain_unspec_ref = True

                    if not(contain_unspec_ref) :               

                        with open("clean_data.json", mode = 'a', encoding = 'utf-8') as fin_file :

                            json.dump(data, fin_file, indent=1)
                            fin_file.write('\n')
                            fin_file.close()

                else :

                    unspecified_ref.append(str(jfile['Message-ID']))

        # Writing all those mails that have None as their References
        else :

            data = {}

            data['Message-ID'] = jfile['Message-ID']
            data['From'] = str(jfile['From'])
            data['To'] = str(jfile['To'])
            data['Cc'] = str(jfile['Cc'])
            data['In-Reply-To'] = str(jfile['In-Reply-To'])
            data['References'] = jfile['References'] 

            with open("clean_data.json", mode = 'a', encoding = 'utf-8') as fin_file :

                json.dump(data, fin_file, indent=1)
                fin_file.write('\n')
                fin_file.close()

    fil.close()