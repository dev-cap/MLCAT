import matplotlib.ticker as ticker
import matplotlib.pyplot as plt

def generate_curve_fit():
    """
    Generatees a panel of graphs comprising of CRT, CL and and RT plots for a range of time periods
    :return: None
    """
    plt.rcParams['font.size'] = 12
    fig = plt.figure(figsize=(7, 7))
    plt.subplots_adjust(wspace=0.05, hspace=0.05)
    ax1 = fig.add_subplot(331)
    ax2 = fig.add_subplot(332)
    ax3 = fig.add_subplot(333)
    ax4 = fig.add_subplot(334)
    ax5 = fig.add_subplot(335)
    ax6 = fig.add_subplot(336)
    ax7 = fig.add_subplot(337)
    ax8 = fig.add_subplot(338)
    ax9 = fig.add_subplot(339)

    foldername = "./data/lkml/curve_fit/FULL_2016/"

    x, y = generate_crt_dist(foldername + 'conversation_refresh_times.csv')
    popt, pcov = curve_fit(inv_func, x, y)
    a, b, c = popt
    # Find RMS error and Normalized-RMS error
    # axes = plt.gca()
    # ax1.set_xlim([0, max(x)])
    # ax1.set_ylim([0, max(y)])
    scale_x = 1e3
    ticks_x = ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x/scale_x))
    ax1.xaxis.set_major_formatter(ticks_x)
    ax1.plot(x, y, linestyle='--', color='b', label="LKML '16")
    x_range = np.linspace(min(x), max(x), 500)
    ax1.plot(x_range, a / x_range + b / (x_range ** 2) + c, 'r-', label="Curve Fit")
    ax1.legend()
    ax1.set_ylabel('pdf')
    ax1.set_xlabel('time (in 10^3 secs)')

    x, y = generate_cl_dist(foldername + 'conversation_length.csv')
    try:
        popt, pcov = curve_fit(inv_func, x, y)
    except:
        print("Cannot fit data to exp in", foldername)
    a, b, c = popt
    # Find RMS error and Normalized-RMS error
    scale_x = 1e3
    ticks_x = ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x/scale_x))
    ax2.xaxis.set_major_formatter(ticks_x)
    ax2.plot(x, y, linestyle='--', color='b', label="LKML '16")
    x_range = np.linspace(min(x), max(x), 500)
    ax2.plot(x_range, a / x_range + b / (x_range ** 2) + c, 'r-', label="Curve Fit")
    ax2.legend()
    ax2.set_ylabel('pdf')
    ax2.set_xlabel('time (in 10^3 secs)')

    x, y = generate_rt_dist(foldername + 'response_time.csv')
    try:
        popt, pcov = curve_fit(inv_func, x, y)
    except:
        print("Cannot fit data to exp in", foldername)
    a, b, c = popt
    # Find RMS error and Normalized-RMS error
    scale_x = 1e3
    ticks_x = ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x/scale_x))
    ax3.xaxis.set_major_formatter(ticks_x)
    ax3.plot(x, y, linestyle='--', color='b', label="LKML '16")
    x_range = np.linspace(min(x), max(x), 500)
    ax3.plot(x_range, a / x_range + b / (x_range ** 2) + c, 'r-', label="Curve Fit")
    ax3.legend()
    ax3.set_ylabel('pdf')
    ax3.set_xlabel('time (in 10^3 secs)')

    foldername = "./data/sakai-devel/curve_fit/FULL_2015/"

    x, y = generate_crt_dist(foldername + 'conversation_refresh_times.csv')
    popt, pcov = curve_fit(inv_func, x, y)
    a, b, c = popt
    # Find RMS error and Normalized-RMS error
    # axes = plt.gca()
    # ax4.set_xlim([0, max(x)])
    # ax4.set_ylim([0, max(y)])
    scale_x = 1e3
    ticks_x = ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x/scale_x))
    ax4.xaxis.set_major_formatter(ticks_x)
    ax4.plot(x, y, linestyle='--', color='b', label="Sakai '15 ")
    x_range = np.linspace(min(x), max(x), 500)
    ax4.plot(x_range, a / x_range + b / (x_range ** 2) + c, 'r-', label="Curve Fit")
    ax4.legend()
    ax4.set_ylabel('pdf')
    ax4.set_xlabel('time (in 10^3 secs)')

    x, y = generate_cl_dist(foldername + 'conversation_length.csv')
    try:
        popt, pcov = curve_fit(inv_func, x, y)
    except:
        print("Cannot fit data to exp in", foldername)
    a, b, c = popt
    # Find RMS error and Normalized-RMS error
    scale_x = 1e3
    ticks_x = ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x/scale_x))
    ax5.xaxis.set_major_formatter(ticks_x)
    ax5.plot(x, y, linestyle='--', color='b', label="Sakai '15")
    x_range = np.linspace(min(x), max(x), 500)
    ax5.plot(x_range, a / x_range + b / (x_range ** 2) + c, 'r-', label="Curve Fit")
    ax5.legend()
    ax5.set_ylabel('pdf')
    ax5.set_xlabel('time (in 10^3 secs)')

    x, y = generate_rt_dist(foldername + 'response_time.csv')
    try:
        popt, pcov = curve_fit(inv_func, x, y)
    except:
        print("Cannot fit data to exp in", foldername)
    a, b, c = popt
    # Find RMS error and Normalized-RMS error
    scale_x = 1e3
    ticks_x = ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x/scale_x))
    ax6.xaxis.set_major_formatter(ticks_x)
    ax6.plot(x, y, linestyle='--', color='b', label="Sakai '15")
    x_range = np.linspace(min(x), max(x), 500)
    ax6.plot(x_range, a / x_range + b / (x_range ** 2) + c, 'r-', label="Curve Fit")
    ax6.legend()
    ax6.set_ylabel('pdf')
    ax6.set_xlabel('time (in 10^3 secs)')

    foldername = "./data/opensuse/curve_fit/FULL_2016/"

    x, y = generate_crt_dist(foldername + 'conversation_refresh_times.csv')
    popt, pcov = curve_fit(inv_func, x, y)
    a, b, c = popt
    # Find RMS error and Normalized-RMS error
    # axes = plt.gca()
    # ax1.set_xlim([0, max(x)])
    # ax1.set_ylim([0, max(y)])
    scale_x = 1e3
    ticks_x = ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x/scale_x))
    ax7.xaxis.set_major_formatter(ticks_x)
    ax7.plot(x, y, linestyle='--', color='b', label="SUSE '16")
    x_range = np.linspace(min(x), max(x), 500)
    ax7.plot(x_range, a / x_range + b / (x_range ** 2) + c, 'r-', label="Curve Fit")
    ax7.legend()
    ax7.set_ylabel('pdf')
    ax7.set_xlabel('time (in 10^3 secs)')

    x, y = generate_cl_dist(foldername + 'conversation_length.csv')
    try:
        popt, pcov = curve_fit(inv_func, x, y)
    except:
        print("Cannot fit data to exp in", foldername)
    a, b, c = popt
    # Find RMS error and Normalized-RMS error
    scale_x = 1e3
    ticks_x = ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x/scale_x))
    ax8.xaxis.set_major_formatter(ticks_x)
    ax8.plot(x, y, linestyle='--', color='b', label="SUSE '16")
    x_range = np.linspace(min(x), max(x), 500)
    ax8.plot(x_range, a / x_range + b / (x_range ** 2) + c, 'r-', label="Curve Fit")
    ax8.legend()
    ax8.set_ylabel('pdf')
    ax8.set_xlabel('time (in 10^3 secs)')

    x, y = generate_rt_dist(foldername + 'response_time.csv')
    try:
        popt, pcov = curve_fit(inv_func, x, y)
    except:
        print("Cannot fit data to exp in", foldername)
    a, b, c = popt
    # Find RMS error and Normalized-RMS error
    scale_x = 1e3
    ticks_x = ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x/scale_x))
    ax9.xaxis.set_major_formatter(ticks_x)
    ax9.plot(x, y, linestyle='--', color='b', label="SUSE '16")
    x_range = np.linspace(min(x), max(x), 500)
    ax9.plot(x_range, a / x_range + b / (x_range ** 2) + c, 'r-', label="Curve Fit")
    ax9.legend()
    ax9.set_ylabel('pdf')
    ax9.set_xlabel('time (in 10^3 secs)')

    fig.tight_layout()
    plt.savefig(foldername + 'snaa.jpg', dpi=300)
    plt.close()
