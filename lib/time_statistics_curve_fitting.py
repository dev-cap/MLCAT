import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def exp_func(x, a, b, c):
    return a * np.exp(-b * x) + c


def generate_crt_dist(csv_filename):
    # Returns Conversation Refresh Times (CRT) as a distribution
    crt_list = list()
    with open(csv_filename) as csv_file:
        next(csv_file)
        for line in csv_file:
            crt_list.append(float(line.split(sep=';')[2]))
    y, bin_edges = np.histogram(crt_list, bins=100)
    count0 = 0
    y = list(y)
    max_y = sum(y)
    y.insert(0, max_y)
    if max_y != 0:
        y = [y1/max_y for y1 in y]
    return list(bin_edges), y


def generate_crt_curve_fits(foldername):
    x, y = generate_crt_dist(foldername+'conversation_refresh_times.csv')
    popt, pcov = curve_fit(exp_func, x, y)
    a, b, c = popt
    # try:
    #     popt, pcov = curve_fit(exp_func, x, y)
    # except:
    #     print("Cannot fit data to exp in", foldername)
    #     return None, None, None
    plt.figure()
    plt.plot(x, y, 'b-', label="Data")
    x_range = np.arange(0, max(x), max(x)/1000)
    plt.plot(x_range, a * np.exp(-b * x_range) + c, 'r-', label="Fitted Curve")
    axes = plt.gca()
    # axes.set_xlim([0, 2000])
    axes.set_ylim([0, 1])
    plt.legend()
    plt.savefig(foldername+'conversation_refresh_times.png')
    plt.close()
    return popt


def generate_cl_dist(csv_filename):
    # Returns Conversation Length (CL) as a distribution
    cl_list = list()
    with open(csv_filename) as csv_file:
        for line in csv_file:
            cl_list.append(float(line.split(sep=';')[1]))
    y, bin_edges = np.histogram(cl_list, bins=100)
    count0 = 0
    y = list(y)
    max_y = sum(y)
    y.insert(0, max_y)
    if max_y != 0:
        y = [y1/max_y for y1 in y]
    return list(bin_edges), y


def generate_cl_curve_fits(foldername):
    x, y = generate_cl_dist(foldername+'conversation_length.csv')
    try:
        popt, pcov = curve_fit(exp_func, x, y)
    except:
        print("Cannot fit data to exp in", foldername)
        return None, None, None
    a, b, c = popt
    plt.figure()
    plt.plot(x, y, 'b-', label="Data")
    x_range = np.arange(0, max(x), max(x)/1000)
    plt.plot(x_range, a * np.exp(-b * x_range) + c, 'r-', label="Fitted Curve")
    axes = plt.gca()
    # axes.set_xlim([0, 2000])
    axes.set_ylim([0, 1])
    plt.legend()
    plt.savefig(foldername+'conversation_length.png')
    plt.close()
    return popt


def generate_rt_dist(csv_filename):
    # Returns Response Time (RT) as a distribution
    rt_list = list()
    with open(csv_filename) as csv_file:
        for line in csv_file:
            rt_list.append(float(line.split(sep=';')[2]))
    y, bin_edges = np.histogram(rt_list, bins=100)
    y = list(y)
    max_y = sum(y)
    y.insert(0, max_y)
    if max_y != 0:
        y = [y1/max_y for y1 in y]
    return list(bin_edges), y


def generate_rt_curve_fits(foldername):
    x, y = generate_rt_dist(foldername+'response_time.csv')
    try:
        popt, pcov = curve_fit(exp_func, x, y)
    except:
        print("Cannot fit data to exp in", foldername)
        return None, None, None
    a, b, c = popt
    plt.figure()
    plt.plot(x, y, 'b-', label="Data")
    x_range = np.arange(0, max(x), max(x)/1000)
    plt.plot(x_range, a * np.exp(-b * x_range) + c, 'r-', label="Fitted Curve")
    axes = plt.gca()
    # axes.set_xlim([0, 2000])
    axes.set_ylim([0, 1])
    plt.legend()
    plt.savefig(foldername+'response_time.png')
    plt.close()
    return popt