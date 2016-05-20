import traceback
import pytz
import datetime
from itertools import islice, chain


def lines_per_n(f, n):
    """
    Each json object in the headers.json file occupies a set number of lines.
    This function is used to read those set number of lines and return them.
    """
    for line in f :
        yield ''.join(chain([line], islice(f, n-1)))


def date_to_UTC(orig_date):
    """
    A function to convert a formatted string containing date and time from a local timezone to UTC, by taking into
    consideration multiple formats of the input parameter
    :param orig_date: Formatted string containing a date and time from a local timezone
    :return: Formatted string containing the date and time in UTC
    """

    try:
        # Truncating the string to contain only required values and removing unwanted whitespace
        trunc_date = orig_date[:31] if len(orig_date) > 31 else orig_date
        trunc_date = trunc_date.strip()

        # Generating a datetime object considering multiple formats of the input parameter - with and without weekday
        if len(trunc_date) > 30 and trunc_date[14] == ':':
            datetime_obj = datetime.datetime.strptime(trunc_date, "%a, %b %d %H:%M:%S %Y %z")
        elif len(trunc_date) == 25 or len(trunc_date) == 26:
            datetime_obj = datetime.datetime.strptime(trunc_date, "%d %b %Y %H:%M:%S %z")
        elif len(trunc_date) == 27 or len(trunc_date) == 28:
            datetime_obj = datetime.datetime.strptime(trunc_date, "%a, %d %b %Y %H:%M %z")
        elif str.isalpha(trunc_date[5]) and str.isdigit(trunc_date[-1]):
            if "CET" in trunc_date:
                trunc_date = trunc_date.replace("CET", "+0100")
            datetime_obj = datetime.datetime.strptime(trunc_date, "%a, %b %d %H:%M:%S %z %Y")
        else:
            datetime_obj = datetime.datetime.strptime(trunc_date, "%a, %d %b %Y %H:%M:%S %z")

        # Converting the datetime object into a formatted string
        utc_dt = datetime_obj.astimezone(pytz.utc)
        return utc_dt.strftime("%a, %d %b %Y %H:%M:%S %z")

    except:
        print("Unable to process date:", orig_date, trunc_date)
        traceback.print_exc()