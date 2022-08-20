from formatting import utils

import datetime

def human_time(post_datetime):
    """
    Function:   human_time
    Definition: The function accepts a given date time object and calculates the difference between the current point
                in time and the time given by the parameter.
                The function then returns a roughly accurate human readable representation of the time difference
    Parameter:  a datetime object ( time posted )
    Return:     a string
    """
    dif = datetime.datetime.now() - post_datetime + datetime.timedelta(hours=8)
    seconds = dif.total_seconds()
    minutes = seconds / 60
    hours = minutes / 60
    if int(hours) < 1:
        return str(int(minutes)) + ' minutes ago'
    elif int(hours) == 1:
        return 'an hour ago'

    days = hours / 24
    if int(days) < 1:
        return str(int(hours)) + ' hours ago'
    elif int(days) == 1:
        return '1 day ago'

    weeks = days / 7
    if int(weeks) < 1:
        return str(int(days)) + ' days ago'
    elif int(weeks) == 1:
        return 'a week ago'

    months = days / 30
    if int(months) < 1:
        return 'over a week ago'
    elif int(months) == 1:
        return 'a month ago'

    years = months / 12
    if int(years) < 1:
        return str(int(months)) + ' months ago'
    elif int(years) == 1:
        return 'a year ago'
    else:
        return str(int(years)) + ' years ago'


def minute_format(num, round_to=2):
    """
    Function:   minute_format
    Definition: The function receives time in seconds which it the converts to minutes using a simple algorithm.
                The remainder is then reconverted back in to seconds and rounds to what ever number is needed
                After, seconds and minutes are formatted according to their value
    Parameter:  num (seconds), round_to (decimal places to round to)
    Return:     a string
    """
    minutes = int(abs(num) / 60)
    seconds = round(abs(num) % 60, round_to)

    if num < 0:         # in the case that the number is negative, write a negative sign
        minutes = '-' + str(minutes)
    if seconds < 10:
        seconds = '0' + str(seconds)
    return str(minutes) + ':' + str(seconds)


def abbreviate_number(num, use_at=1000):
    """
    Function:   abbreviate_number
    Definition: This function takes a given number and shortens it.
                eg. 1000000 becomes 1M, and 1000 becomes 1k
    Parameter:  num
    Return:     an abbreviated string of the original number
    """
    if num >= use_at:
        magnitude = 0
        while abs(num) >= 1000:
            magnitude += 1
            num /= 1000.0
        return '%.1f%s' % (num, ['', 'k', 'M', 'G', 'T', 'P'][magnitude])  # suffixes
    else:
        return str(num)
