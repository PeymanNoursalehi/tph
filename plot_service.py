from collections import Counter
import textwrap

import matplotlib.pyplot as plt
import numpy as np

def make_labels(rects, ax):
    for rect in rects:
        height = int(rect.get_height())
        if height == 0:
            continue
        elif (height >= 2):
            bar_text = str(height)
            yloc = rect.get_y() + (rect.get_height() / 2.0)
            xloc = rect.get_x() + (rect.get_width() / 2.0)
            ax.text(xloc, yloc, bar_text, horizontalalignment='center',
                     verticalalignment='center', color='white', weight='bold', size='x-small')


def make_top_labels(rects, ax, total):
    for rect in rects:
        bar_text = int(total[int(rect.get_x())])
        yloc = rect.get_y() + rect.get_height() + 2
        xloc = rect.get_x() + (rect.get_width() / 2.0)
        ax.text(xloc, yloc, bar_text, horizontalalignment='center',
                 verticalalignment='center', color='black', weight='bold', size='x-small')


def plot_service(results, target_stop_name, target_date, outfile):
    maxtph = 60 #TODO: set this automagically
    HOURS = 24

    fig = plt.figure(figsize=(16,6), dpi=300)
    ax = fig.add_subplot(111, xlim=(0,24), ylim=(0, maxtph))
    fig.subplots_adjust(bottom = 0.2, left=0.05, right=0.98)
    
    pos = np.arange(HOURS)
    width = 0.40

    ax.set_xlabel('Hour')
    ax.set_ylabel('Vehicles per Hour')
    ax.set_title('Service at %s on %s' % (target_stop_name, target_date.strftime("%Y-%m-%d")))
    ax.set_yticks(np.arange(0, maxtph, 4))
    ax.set_xticks(pos+width)
    ax.set_xticklabels([str(i) for i in range(0, HOURS)])

    color_dups = Counter()
    hatch = ["/", "O", "x", "o", ".", "*"]

    values_0 = np.array(np.zeros(HOURS))
    values_1 = np.array(np.zeros(HOURS))

    for route_id, route_data in results.items():
        plt_args = {}
        if route_data['route_color'] != '':
            plt_args['color'] = '#' + route_data['route_color']
        else:
            plt_args['color'] = '#ffffff'
        color_dups[plt_args['color']] += 1
        if color_dups[plt_args['color']] > 1:
            plt_args['hatch'] = hatch[color_dups[plt_args['color']] - 2]
        route_data['plot_0'] = ax.bar(pos, route_data['bins_0'], width, bottom=values_0, **plt_args)
        route_data['plot_1'] = ax.bar(pos+width, route_data['bins_1'], width, bottom=values_1, **plt_args)

        make_labels(route_data['plot_0'], ax)
        make_labels(route_data['plot_1'], ax)

        values_0 += np.array(route_data['bins_0'])
        values_1 += np.array(route_data['bins_1'])


    last_route_data = results.values()[-1]
    make_top_labels(last_route_data['plot_0'], ax, values_0)
    make_top_labels(last_route_data['plot_1'], ax, values_1)

    plt.legend([route_data['plot_0'][0] for route_data in results.values()],
               [route_data['route_name'] for route_data in results.values()])

    headsigns_0 = set()
    headsigns_1 = set()

    for route in results.values():
        headsigns_0.update(route['headsigns_0'].keys())
        headsigns_1.update(route['headsigns_1'].keys())

    d0 = textwrap.fill("Direction 0 is: %s" % (", ".join(headsigns_0)), 170, subsequent_indent='    ')
    d1 = textwrap.fill("Direction 1 is: %s" % (", ".join(headsigns_1)), 170, subsequent_indent='    ')

    plt.figtext(0.05, 0.05, d0+"\n"+d1, size="small")

    plt.savefig(outfile)