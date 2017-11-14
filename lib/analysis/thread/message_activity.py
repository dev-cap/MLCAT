import plotly as ply
import plotly.graph_objs as plygo
from util.read import *
import json


def generate_weekly_message_activity_heatmap(json_data, filename):
    """
    Generate weekly message activity heatmap from JSON data.

    :param json_data: Data for generating the heatmap.
    :param filename: Heatmap file name.
    """
    heatmap_data = [[0 for x in range(48)] for x in range(7)]
    for msg_uid, json_obj in json_data.items():
        sent_day = json_obj['Time'].weekday()
        bin_number = 2*json_obj['Time'].hour if json_obj['Time'].minute < 30 else 2*json_obj['Time'].hour+1
        heatmap_data[sent_day][bin_number] += 1
    heatmap = [plygo.Heatmap(
        z=heatmap_data,
        x=list(range(48)),
        y=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])]
    ply.offline.plot(heatmap, filename=filename)


def generate_monthly_message_activity_heatmap(json_data, filename):
    """
    Generate monthly message activity heatmap from JSON data.

    :param json_data: Data for generating the heatmap.
    :param filename: Heatmap file name.
    """
    heatmap_data = [[0 for x in range(48)] for x in range(12)]
    for msg_uid, json_obj in json_data.items():
        sent_month = json_obj['Time'].month-1
        bin_number = 2*json_obj['Time'].hour if json_obj['Time'].minute < 30 else 2*json_obj['Time'].hour+1
        heatmap_data[sent_month][bin_number] += 1
    heatmap = [plygo.Heatmap(
        z=heatmap_data,
        x=list(range(48)),
        y=list(range(1,12)))]
    ply.offline.plot(heatmap, filename=filename)


def generate_daily_message_activity_timeline(json_data, filename):
    """
    Generate daily message activity timeline from JSON data.

    :param json_data: Data for generating the timeline.
    :param filename: Timeline file name.
    """
    timeline_data = [0 for x in range(48)]
    for msg_uid, json_obj in json_data.items():
        bin_number = 2*json_obj['Time'].hour if json_obj['Time'].minute < 30 else 2*json_obj['Time'].hour+1
        timeline_data[bin_number] += 1
    trace = plygo.Scatter(
        x=list(range(48)),
        y=timeline_data
    )
    timeline = [trace]
    ply.offline.plot(timeline, filename=filename)


def generate_weekly_message_activity_timeline(json_data, filename):
    """
    Generate weekly message activity timeline from JSON data.

    :param json_data: Data for generating the timeline.
    :param filename: Timeline file name.
    """
    timeline_data = [0 for x in range(7*24)]
    for msg_uid, json_obj in json_data.items():
        bin_number = json_obj['Time'].hour + 24 * json_obj['Time'].weekday()
        timeline_data[bin_number] += 1
    trace = plygo.Scatter(
        x=list(range(7*24)),
        y=timeline_data
    )
    timeline = [trace]
    ply.offline.plot(timeline, filename=filename)


def generate_monthly_message_activity_timeline(json_data, filename):
    """
    Generate monthly message activity timeline from JSON data.

    :param json_data: Data for generating the timeline.
    :param filename: Timeline file name.
    """	
    timeline_data = [0 for x in range(31*24)]
    for msg_uid, json_obj in json_data.items():
        bin_number = json_obj['Time'].hour + 24 * (json_obj['Time'].day - 1)
        timeline_data[bin_number] += 1
    trace = plygo.Scatter(
        x=list(range(31*24)),
        y=timeline_data
    )
    timeline = [trace]
    ply.offline.plot(timeline, filename=filename)


def generate_yearly_message_activity_timeline(json_data, filename):
    """
    Generate yearly message activity timeline from JSON data.

    :param json_data: Data for generating the timeline.
    :param filename: Timeline file name.
    """
    timeline_data = [0 for x in range(366*24)]
    for msg_uid, json_obj in json_data.items():
        bin_number = json_obj['Time'].hour + 24 * (json_obj['Time'].timetuple().tm_yday - 1)
        timeline_data[bin_number] += 1
    trace = plygo.Scatter(
        x=list(range(365*24)),
        y=timeline_data
    )
    timeline = [trace]
    ply.offline.plot(timeline, filename=filename)


def generate_message_activity_heatmaps(clean_headers_filename, foldername, timeline=True):
    """
    Extract header information and call functions to generate various timelines or heatmaps.

    :param clean_headers_filename: The JSON file containing cleaned headers.
    :param foldername: The MBOX folder.
    :param timeline: True for generating timelines,False for heatmaps.
    """
    # Time limit can be specified here in the form of a timestamp in one of the identifiable formats. All messages
    # that have arrived after time_ubound and before time_lbound will be ignored.
    time_ubound = None
    time_lbound = None

    # If ignore_lat is true, then messages that belong to threads that have only a single author are ignored.
    ignore_lat = False

    author_graph = nx.DiGraph()
    email_re = re.compile(r'[\w\.-]+@[\w\.-]+')
    json_data = dict()

    if time_ubound is None:
        time_ubound = time.strftime("%a, %d %b %Y %H:%M:%S %z")
    time_ubound = get_datetime_object(time_ubound)

    if time_lbound is None:
        time_lbound = "Sun, 01 Jan 2001 00:00:00 +0000"
    time_lbound = get_datetime_object(time_lbound)

    print("All messages before", time_ubound, "and after", time_lbound,  "are being considered.")

    if not ignore_lat:
        with open(clean_headers_filename, 'r') as json_file:
            for chunk in lines_per_n(json_file, 9):
                json_obj = json.loads(chunk)
                json_obj['Message-ID'] = int(json_obj['Message-ID'])
                json_obj['Time'] = datetime.datetime.strptime(json_obj['Time'], "%a, %d %b %Y %H:%M:%S %z")
                if time_lbound <= json_obj['Time'] < time_ubound:
                    # print("\nFrom", json_obj['From'], "\nTo", json_obj['To'], "\nCc", json_obj['Cc'])
                    from_addr = email_re.search(json_obj['From'])
                    json_obj['From'] = from_addr.group(0) if from_addr is not None else json_obj['From']
                    json_obj['To'] = set(email_re.findall(json_obj['To']))
                    json_obj['Cc'] = set(email_re.findall(json_obj['Cc'])) if json_obj['Cc'] is not None else None
                    # print("\nFrom", json_obj['From'], "\nTo", json_obj['To'], "\nCc", json_obj['Cc'])
                    json_data[json_obj['Message-ID']] = json_obj
    else:
        lone_author_threads = get_lone_author_threads(save_file=None, nodelist_filename=foldername+"/tables/graph_nodes.csv", edgelist_filename=foldername+"/tables/graph_edges.csv")
        with open(clean_headers_filename, 'r') as json_file:
            for chunk in lines_per_n(json_file, 9):
                json_obj = json.loads(chunk)
                json_obj['Message-ID'] = int(json_obj['Message-ID'])
                if json_obj['Message-ID'] not in lone_author_threads:
                    json_obj['Time'] = datetime.datetime.strptime(json_obj['Time'], "%a, %d %b %Y %H:%M:%S %z")
                    if time_lbound <= json_obj['Time'] < time_ubound:
                        # print("\nFrom", json_obj['From'], "\nTo", json_obj['To'], "\nCc", json_obj['Cc'])
                        from_addr = email_re.search(json_obj['From'])
                        json_obj['From'] = from_addr.group(0) if from_addr is not None else json_obj['From']
                        json_obj['To'] = set(email_re.findall(json_obj['To']))
                        json_obj['Cc'] = set(email_re.findall(json_obj['Cc'])) if json_obj['Cc'] is not None else None
                        # print("\nFrom", json_obj['From'], "\nTo", json_obj['To'], "\nCc", json_obj['Cc'])
                        json_data[json_obj['Message-ID']] = json_obj
    print("JSON data loaded.")

    if not timeline:
        generate_weekly_message_activity_heatmap(json_data, foldername+'/heatmaps/weekly-message-activity-heatmap.html')
        generate_monthly_message_activity_heatmap(json_data, foldername+'/heatmaps/monthly-message-activity-heatmap.html')
    else:
        generate_daily_message_activity_timeline(json_data, foldername + '/plots/daily-message-activity-timeline.html')
        generate_weekly_message_activity_timeline(json_data, foldername + '/plots/weekly-message-activity-timeline.html')
        generate_monthly_message_activity_timeline(json_data, foldername + '/plots/monthly-message-activity-timeline.html')
        generate_yearly_message_activity_timeline(json_data, foldername + '/plots/yearly-message-activity-timeline.html')
