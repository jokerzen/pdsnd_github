#!/usr/bin/env python
"""
Submitted for your approval
"""

from calendar import month_name, day_name
import json
import sys
import time
import pandas as pd


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

# https://www.tutorialsrack.com/articles/207/how-to-get-a-month-name-using-the-month-number-in-python
MONTHS = [ 'all'] + [ month_name[(i)].lower() for i in range(1, 7)]
DAYS = [ 'all'] + [ day_name[(i)].lower() for i in range(0, 7)]
ST='Start Time'
SS='Start Station'
ES='End Station'
TD='Trip Duration'
UT='User Type'
GE='Gender'
BY='Birth Year'

def get_help(help_list):
    """Display list of options for the menu"""
    print('q) quit')
    i = 1
    for k in help_list:
        if k == 'all':
            print('a) all')
            continue
        print("{}) {}".format(i, k))
        i += 1

def get_input(help_list, selection, last, allind = False):
    """
    Wrapper around input to allow input valid values from user

    Returns:
        Will exit app if user inputs 'q'
        Will display help if user inputs '?'
        (int) the index in the list of valid selections, or -1 for 'all'
    """
    allstr, allerr = '', ''
    if allind:
        allstr = '[a], '
        allerr = ", or 'a' for all"
        last = last - 1
    ind = -1
    while True:
        try:
            resp = input("Select {} (?, q, {}1-{}): ".format(selection, allstr, last))
            if resp == '?':
                get_help(help_list)
                continue
            if resp == 'q':
                sys.exit()
            if allind and (resp in ('a', '')):
                return 0
            ind = int(resp)
            if 0 < ind <= last:
                if allind:
                    return ind
                return ind - 1
            raise ValueError
        except ValueError:
            print("values must be a number between 1 and {} or 'q' for quit{}".format(last, allerr))

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington).
    i = 1
    for k in CITY_DATA:
        print("{}) {}".format(i, k))
        i += 1

    cities = CITY_DATA.keys()
    city = list(cities)[ get_input(CITY_DATA, 'city', len(cities)) ]

    # get user input for month (all, january, february, ... , june)

    # print("MONTHS {}".format(MONTHS))
    month = MONTHS[ get_input(MONTHS, 'month', len(MONTHS), allind = True) ]

    # get user input for day of week (all, monday, tuesday, ... sunday)
    # print("DAYS {}".format(DAYS))
    day = DAYS[ get_input(DAYS, 'day', len(DAYS), allind = True) ]

    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(city.replace(' ', '_') + '.csv')

    if month != 'all':
        # https://kanoki.org/2019/11/12/how-to-use-regex-in-pandas/
        # https://stackoverflow.com/questions/176918/finding-the-index-of-an-item-in-a-list
        df = df[ df[ST].str.match('^....-0?{}.*'.format(MONTHS.index(month))) ]

    if day != 'all':
        # https://stackoverflow.com/questions/33365055/attributeerror-can-only-use-dt-accessor-with-datetimelike-values
        # https://www.timeanddate.com/calendar/?year=2017
        df = df[ pd.to_datetime(df[ST]).dt.dayofweek == DAYS.index(day) - 1 ]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    # https://stackoverflow.com/questions/15138973/how-to-get-the-number-of-the-most-frequent-value-in-a-column
    common_month = pd.to_datetime(df[ST]).dt.month.value_counts().idxmax()
    print("The most common month {}({})".format(MONTHS[common_month].title(), common_month))

    # display the most common day of week
    common_day = pd.to_datetime(df[ST]).dt.dayofweek.value_counts().idxmax()
    print("The most common day of week {}({})".format(DAYS[common_day].title(), common_day))

    # display the most common start hour
    print("The most common start hour {}".format(
        pd.to_datetime(df[ST]).dt.hour.value_counts().idxmax()
    ))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("The most common ({}) start station '{}'".format(
        df[SS].value_counts().max(),
        df[SS].value_counts().idxmax()
    ))

    # display most commonly used end station
    print("The most common ({}) end station '{}'".format(
        df[ES].value_counts().max(),
        df[ES].value_counts().idxmax()
    ))

    # display most frequent combination of start station and end station trip
    print("The most common end station '{}'".format(
        (df[SS] + ' ' + df[ES]).value_counts().idxmax()
    ))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.sum.html
    print("The total travel time {}".format(
        df[TD].sum()
    ))

    # display mean travel time
    print("The mean travel time {}".format(
        df[TD].mean()
    ))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    # https://stackoverflow.com/questions/53025207/how-do-i-remove-name-and-dtype-from-pandas-output
    print("The counts of user types:\n{}\n".format(
        df[UT].value_counts().to_string()
    ))

    # Display counts of gender
    # https://stackoverflow.com/questions/24870306/how-to-check-if-a-column-exists-in-pandas
    if GE in df:
        print("The counts of gender:\n{}\n".format(
            df[GE].value_counts().to_string()
        ))
    else:
        print("Gender data was not collected for this city.\n")

    # Display earliest, most recent, and most common year of birth
    # https://stackoverflow.com/questions/21291259/convert-floats-to-ints-in-pandas
    if BY in df:
        list_or_val = list(df[BY].mode().astype(int))
        if len(list_or_val) == 1:
            val = list_or_val[0]
        else:
            val= list_or_val
        print("The earliest: {}, most recent: {}, and most common year of birth: {}".format(
            int(df[BY].min()),
            int(df[BY].max()),
            val
        ))
    else:
        print("Birth Year data was not collected for this city.\n")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def show_raw(df):
    """Displays 5 rows of raw data at a time."""
    restart = input('\nWould you like to view the raw data? Enter yes or [no].\n')
    if restart.lower() != 'yes':
        return

    print('\n-- RAW DATA --')
    till = 5

    while True:
        group = json.loads(df[till - 5:till].to_json(orient='index'))
        for k in group.keys():
            print(json.dumps(group[k], indent = 2))

        if till >= len(df):
            print('\n-- LAST RECORD --')
            break
        till += 5

        restart = input('\nWould you like to continue? Enter yes or [no].\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    """ Main loop to run each function """
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        if len(df) == 0:
            if month != 'all':
                month_error = ' in ' + month.title()
            if day != 'all':
                day_error = ' on ' + day.title() + 's'
            print('\nThere is no data for {}{}{}'.format(city, month_error, day_error))
        else:
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)

            show_raw(df)

        restart = input('\nWould you like to restart? Enter yes or [no].\n')
        if restart.lower() != 'yes':
            break

