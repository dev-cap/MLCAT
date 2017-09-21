import configparser
import imaplib

"""
Gmail uses OAuth for authentications purposes. This means that a regular SSL connection request
is refused by the mail server. So we have change the account settings to allow for access from less
secure applications.
"""


def open_connection(verbose=False):
    """
    Function to establish to mail server and login to user account using IMAP4 protocol.
    Returns the connection object used in establishing IMAP connection to mail server.
    Takes as argument boolen value which is used to determine whether function works in
    verbose mode or not.
    
    :param verbose: Displays a detailed log if true.
    """

    # Reading from config file
    config = configparser.ConfigParser()
    config.read("imap.config")

    # Creating connection to mail server using IMAP protocol
    hostname = config.get('server', 'hostname')

    if verbose:
        print('Connecting to ', hostname, ' ...')

    connection = imaplib.IMAP4_SSL(hostname)

    # Logging in using credentials in config file
    username = config.get('account', 'username')
    password = config.get('account', 'password')

    if verbose:
        print('Logging in as ', username, ' ...')

    connection.login(username, password)

    # Returning connection object
    return connection
