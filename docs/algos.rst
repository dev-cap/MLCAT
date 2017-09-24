Algorithms for Parsing Mailing Lists
=====================================

This section shows the function calls to Fetch Headers from IMAP Server which can be run by executing the driver file - fetch_headers.py

1. check_headers.check_validity()
    - Returns last_uid_read
    - Identifies unavailable (in the IMAP server), duplicate, missing (from the JSON file), invalid and unwanted headers

2. check_headers.remove_duplicate_headers(to_remove=duplicate_uid)

    2.1 util.read_json.lines_per_n()
        - This function is used to read a set number of lines from a JSON file and return them

3. check_headers.remove_unwanted_headers(to_remove=unwanted_uid)

    3.1 util.read_json.lines_per_n()

4. check_headers.add_missing_headers(to_add=missing_uid)

    4.1 imap_hdr.get_mail_header(list_of_headers_to_get, range_=True)

        4.1.1 imap_hdr.init_uid_map() 

        4.1.2 imap_conn.open_connection()

        4.1.3 imap_hdr.date_to_utc()

        4.1.4 encoder.NoIndent()

5. check_headers.replace_invalid_headers((to_replace=invalid_uid)

    5.1 util.read_json.lines_per_n()

    5.2 add_missing_headers(to_add=to_replace)

        5.2.1 imap_hdr.get_mail_header(list_of_headers_to_get, range_=True)

            5.2.1.1 imap_hdr.init_uid_map()

            5.2.1.2 imap_conn.open_connection()

            5.2.1.3 imap_hdr.date_to_utc()

            5.2.1.4 encoder.NoIndent()

6. imap_hdr.get_mail_header(list_of_headers_to_get, range_=True)

    6.1 imap_hdr.init_uid_map()
        - Returns a map with the string in the Message-Id field of the header to the UID of the mail is required
        - The mapping is required to ensure that references are correctly recorded in the JSON file such that there are no references to mails that do not exist and to ease the processing of headers.

    6.2 imap_conn.open_connection()
        - Function to establish connection to the mail server and login to user account using IMAP4 protocol.
        - Returns the connection object used in establishing IMAP connection to mail server.

    6.3 imap_hdr.date_to_utc()
        - Converts a formatted string containing date and time from a local timezone to UTC.

    6.4 encoder.NoIndent()
        - Converts a list into a string of comma separated elements of the list for pretty printing.

7. data_cleanup.remove_invalid_references()

    7.1 util.read_json.lines_per_n()
