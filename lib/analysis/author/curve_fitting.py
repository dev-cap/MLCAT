import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from scipy.optimize import curve_fit
plt.rcParams['font.size'] = 14

def inv_func(x, a, b, c):
	"""
	The model function used for curve fitting.

	"""
	return a/x + b/(x**2) + c
	

def generate_crt_dist(csv_filename):
    """
    Generates distribution for conversation refresh times from a csv.

    :param csv_filename: The csv filename as a parameter
    :return: Conversation Refresh Times(CRT) as a distribution.
    """
    crt_list = list()
    with open(csv_filename) as csv_file:
        next(csv_file)
        for line in csv_file:
            crt_list.append(float(line.split(sep=';')[2]))
    y, bin_edges = np.histogram(sorted(crt_list)[:int(0.9*len(crt_list))], bins=50)
    y = list(y)
    x1 = list(bin_edges)
    x = list()
    for i1 in range(len(x1) - 1):
        x.append((x1[i1] + x1[i1 + 1]) / 2)
    max_y = sum(y)
    if max_y != 0:
        y = [y1/max_y for y1 in y]
    return x, y


def generate_crt_curve_fits(foldername):
    """
    Generates curve fits for conversation refresh times distribution and saves it as a PNG.

    :param foldername: Folder name as a parameter
    :return popt: An array containging optimal values for the parameters.
    :return rms: Mean squared error.
    """
    x, y = generate_crt_dist(foldername+'conversation_refresh_times.csv')
    popt, pcov = curve_fit(inv_func, x, y)
    a, b, c = popt
    # Find RMS error and Normalized-RMS error
    rms =  mean_squared_error(inv_func(np.array(x), *popt), y)
    plt.figure()
    axes = plt.gca()
    axes.set_xlim([0, max(x)])
    axes.set_ylim([0, max(y)])
    plt.plot(x, y, linestyle='--', color='b', label="Data")
    x_range = np.linspace(min(x), max(x), 500)
    plt.plot(x_range, a / x_range + b / (x_range ** 2) + c, 'r-', label="Fitted Curve")
    plt.legend()
    plt.ylabel('pdf')
    plt.xlabel('time (in secs)')
    plt.savefig(foldername+'/conversation_refresh_times.png')
    plt.close()
    return popt, rms


def generate_cl_dist(csv_filename):
    """
    Generates distribution for conversation lengths from a csv.

    :param csv_filename: The csv filename as a parameter
    :return: Conversation Length (CL) as a distribution
    """
    cl_list = list()
    with open(csv_filename) as csv_file:
        for line in csv_file:
            cl_list.append(float(line.split(sep=';')[1]))
    y, bin_edges = np.histogram(sorted(cl_list)[:int(0.9*len(cl_list))], bins=50)
    y = list(y)
    x1 = list(bin_edges)
    x = list()
    for i1 in range(len(x1) - 1):
        x.append((x1[i1] + x1[i1 + 1]) / 2)
    max_y = sum(y)
    if max_y != 0:
        y = [y1 / max_y for y1 in y]
    return x, y


def generate_cl_curve_fits(foldername):
    """
    Generates curve fits for conversation length distribution and saves it as a PNG.

    :param foldername: Folder name as a parameter
    :return popt: An array containging optimal values for the parameters.
    :return rms: Mean squared error.
    """
    x, y = generate_cl_dist(foldername+'conversation_length.csv')
    try:
        popt, pcov = curve_fit(inv_func, x, y)
    except:
        print("Cannot fit data to exp in", foldername)
        return None, None, None
    a, b, c = popt
    # Find RMS error and Normalized-RMS error
    rms =  mean_squared_error(inv_func(np.array(x), *popt), y)**2
    plt.figure()
    axes = plt.gca()
    axes.set_xlim([0, max(x)])
    axes.set_ylim([0, max(y)])
    plt.plot(x, y, linestyle='--', color='b', label="Data")
    x_range = np.linspace(min(x), max(x), 500)
    plt.plot(x_range, a / x_range + b / (x_range ** 2) + c, 'r-', label="Fitted Curve")
    plt.legend()
    plt.ylabel('pdf')
    plt.xlabel('time (in secs)')
    plt.savefig(foldername+'/conversation_length.png')
    plt.close()
    return popt, rms


def generate_rt_dist(csv_filename):
    """
    Generates distribution for refresh times from a csv.

    :param csv_filename: The csv filename as a parameter
    :return: Refresh Times(RT) as a distribution.
    """
    rt_list = list()
    with open(csv_filename) as csv_file:
        for line in csv_file:
            rt_list.append(float(line.split(sep=';')[2]))
    y, bin_edges = np.histogram(sorted(rt_list)[:int(0.9*len(rt_list))], bins=50)
    y = list(y)
    x1 = list(bin_edges)
    x = list()
    for i1 in range(len(x1) - 1):
        x.append((x1[i1] + x1[i1 + 1]) / 2)
    max_y = sum(y)
    if max_y != 0:
        y = [y1 / max_y for y1 in y]
    return x, y


def generate_rt_curve_fits(foldername):
    """
    Generates curve fits for refresh times distribution and saves it as a PNG.

    :param foldername: Folder name as a parameter
    :return popt: An array containging optimal values for the parameters.
    :return rms: Mean squared error.
    """
    x, y = generate_rt_dist(foldername+'response_time.csv')
    try:
        popt, pcov = curve_fit(inv_func, x, y)
    except:
        print("Cannot fit data to exp in", foldername)
        return None, None, None
    a, b, c = popt
    # Find RMS error and Normalized-RMS error
    rms =  mean_squared_error(inv_func(np.array(x), *popt), y)**2
    plt.figure()
    axes = plt.gca()
    axes.set_xlim([0, max(x)])
    axes.set_ylim([0, max(y)])
    plt.plot(x, y, linestyle='--', color='b', label="Data")
    x_range = np.linspace(min(x), max(x), 500)
    plt.plot(x_range, a / x_range + b / (x_range ** 2) + c, 'r-', label="Fitted Curve")
    plt.legend()
    plt.ylabel('pdf')
    plt.xlabel('time (in secs)')
    plt.savefig(foldername+'/response_time.png')
    plt.close()
    return popt, rms
