import math

def hour_to_time(hour):
    return "%2i:%02i" % (math.floor(hour), (hour - math.floor(hour)) * 60)


def plot_spacing(intervals, spacing, worstspacing):
    print 'Service period -  Spacing'
    for i in range(len(intervals)-1):
        # heuristic: if worst spacing is greater than 1.25 x median spacing, print it also
        if spacing[i] == float("inf"):
            spacingstr = "No service"
        else:
            spacingstr = str(int(spacing[i]))
            if float(worstspacing[i]) / float(spacing[i]) > 1.25:
                spacingstr = spacingstr + ' - ' + str(int(worstspacing[i]))
            spacingstr = spacingstr + ' min'
        print '%s - %s ... %s' % (hour_to_time(intervals[i]),
                                  hour_to_time(intervals[i+1]), spacingstr)