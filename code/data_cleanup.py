from itertools import islice, chain
import json


def lines_per_n(f, n):
    """
    Each json object in the headers.json file occupies a set number of lines.
    This function is used to read those set number of lines and return them.
    """
    for line in f :
        yield ''.join(chain([line], islice(f, n-1)))


def remove_invalid_references():

    # The "unspecified_ref" list is used to keep track of all those mails that have '0' in their reference list.
    # If any mail has any of the element in this list in its list of references, we can eliminate them as well
    unspecified_ref = ['0']

    print("Removing headers associated with invalid references...")

    with open('headers.json', 'r') as fil:
        with open("clean_data.json", mode='w', encoding='utf-8') as fin_file :

            for chunk in lines_per_n(fil, 9):
                # The "jfile" is used to store the json object read from the file.
                jfile = json.loads(chunk)

                """
                Mails that have references that are of type None indicate that they maybe the start of threads.
                Anything else could be mail in a thread or something else.
                """
                if not jfile['References'] is None:

                    # Checking if the references is an empty string
                    if not jfile['References'] == "":

                        # The references are stored as a comma separated string. We have to split it at the ',' to get a list.
                        ref_list = jfile['References'].split(',')

                        # A '0' in the list indicates that the mail contains references to some other mail which is not available to us
                        if not('0' in ref_list) :

                            data = {}
                            data['Message-ID'] = jfile['Message-ID']
                            data['From'] = str(jfile['From'])
                            data['To'] = str(jfile['To'])
                            data['Cc'] = str(jfile['Cc'])
                            data['In-Reply-To'] = str(jfile['In-Reply-To'])
                            data['References'] = str(jfile['References'])
                            data['Time'] = str(jfile['Time'])
                            contain_unspec_ref = False

                            # This is done to eliminate all those mails whose reference list contains mails that have '0' in their reference list
                            for ref in ref_list :
                                if ref in unspecified_ref :
                                    contain_unspec_ref = True

                            if not contain_unspec_ref:
                                    json.dump(data, fin_file, indent=1)
                                    fin_file.write('\n')

                        else:
                            unspecified_ref.append(str(jfile['Message-ID']))

                # Writing all those mails that have None as their References
                else:
                    data = {}
                    data['Message-ID'] = jfile['Message-ID']
                    data['From'] = str(jfile['From'])
                    data['To'] = str(jfile['To'])
                    data['Cc'] = str(jfile['Cc'])
                    data['In-Reply-To'] = str(jfile['In-Reply-To'])
                    data['References'] = jfile['References']
                    data['Time'] = str(jfile['Time'])
                    json.dump(data, fin_file, indent=1)
                    fin_file.write('\n')

        fin_file.close()
    fil.close()