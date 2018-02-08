import json
from util.read import lines_per_n


def remove_invalid_references(input_json_filename, output_json_filename, ref_toggle=False):
    """
    This function is used to remove headers associated with invalid references.
    
    :param input_json_filename: The json file containing all the references.
    :param output_json_filename: The output json without invalid references.
    :param ref_toggle: If true, gets the reference list from 'References' attribute.
    """

    # The "unspecified_ref" list is used to keep track of all those mails that have '0' in their reference list.
    # If any mail has any of the element in this list in its list of references, we can eliminate them as well
    unspecified_ref = ['0']

    print("Removing headers associated with invalid references...")

    with open(input_json_filename, 'r') as fil:
        with open(output_json_filename, mode='w', encoding='utf-8') as fin_file :

            for chunk in lines_per_n(fil, 9):
                # The "jfile" is used to store the json object read from the file.
                jfile = json.loads(chunk)

                """
                Mails that have references that are of type None indicate that they maybe the start of threads.
                Anything else could be mail in a thread or something else.
                """
                if jfile['References'] is not None:
                    # Checking if the references is an empty string
                    if not jfile['References'] == "":
                        # The references are stored as a comma separated string. We have to split it at the ',' to get a list.
                        if ref_toggle:
                            ref_list = jfile['References'].split(',')
                        else:
                            if jfile['In-Reply-To'] is not None:
                                ref_list = [str(jfile['In-Reply-To'])]
                            else:
                                ref_list = None
                        # A '0' in the list indicates that the mail contains references to some other mail which is not available to us
                        if '0' not in ref_list or ref_list is None:
                            data = {}
                            data['Message-ID'] = jfile['Message-ID']
                            data['From'] = jfile['From']
                            data['To'] = jfile['To']
                            data['Cc'] = jfile['Cc']
                            data['In-Reply-To'] = jfile['In-Reply-To']
                            data['References'] = jfile['References']
                            data['Time'] = jfile['Time']
                            contain_unspec_ref = False

                            # This is done to eliminate all those mails whose reference list contains mails that have '0' in their reference list
                            for ref in ref_list :
                                if ref in unspecified_ref:
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
                    data['From'] = jfile['From']
                    data['To'] = jfile['To']
                    data['Cc'] = jfile['Cc']
                    data['In-Reply-To'] = jfile['In-Reply-To']
                    data['References'] = jfile['References']
                    data['Time'] = str(jfile['Time'])
                    json.dump(data, fin_file, indent=1)
                    fin_file.write('\n')

        fin_file.close()
    fil.close()
