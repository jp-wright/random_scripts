import datetime as dte
import re
import sys


def get_mins_worked(time_range, sesh):
    """
    Takes in a time range (or ranges) and returns the total minutes between the two times.  Will return cumulative minutes totaled if multiple ranges given.
    INPUT: Time range in the format "hh:mm - hh:mm", with multiple ranges separated by a comma: "hh:mm - hh:mm, hh:mm - hh:mm" etc.  Input need not be enclosed in quotes and spaces are unimportant.
    OUTPUT: Minutes between time ranges.
    """
    start_day, end_day = dte.date(2000, 1, 1), dte.date(2000, 1, 1)
    times = re.findall(r'\d{1,2}:\d{1,2}', str(time_range))
    start_time = dte.time(*[int(num) for num in re.findall(r'\d{1,2}', times[0])])
    end_time = dte.time(*[int(num) for num in re.findall(r'\d{1,2}', times[1])])
    if end_time.hour < start_time.hour:
        end_day += dte.timedelta(1)

    # timedelta returns seconds, div by 60 to give minutes *in sec pos*
    mins_worked = ((dte.datetime.combine(end_day, end_time) - dte.datetime.combine(start_day, start_time)) / 60).seconds
    time_worked = divmod(mins_worked, 60)

    print("You worked {hr}h, {mn}m during session {sesh}.".format(hr=time_worked[0], mn=time_worked[1], sesh=sesh))
    return mins_worked


def show_time_worked(sesh):
    """
    Reports time in hours and minutes between any number of time ranges by calling (repeatedly if necessary) the 'get_mins_worked' function.
    INPUT: Defaults of mins, time_ranges, sesh
    OUTPUT: time in hours and minutes
    """
    mins = 0
    time_ranges = list()
    time_range = input("Enter time range in 'hh:mm - hh:mm' format (enter 'F' to quit): ")
    if time_range.lower() == 'f':
        sys.exit()
    elif "," in time_range:
        try:
            time_ranges = time_range.split(",")
            for time_range in time_ranges:
                mins += get_mins_worked(time_range, sesh)
                sesh += 1
        except IndexError:
            print("An incomplete time range was entered. Proceeding with only complete time range(s).")
    else:
        try:
            mins += get_mins_worked(time_range, sesh)
        except IndexError:
            print("Incorrect time range entered.  Please try again.")
            mins = show_time_worked(sesh)

    return mins

if __name__ == '__main__':
    sesh = 1
    mins = show_time_worked(sesh)
    hr_mn = divmod(mins, 60)
    print("Total time worked today: {hr}h, {mn}m. \nCongrats, I'm really impressed. You're my hero'.".format(hr=hr_mn[0], mn=hr_mn[1]))
