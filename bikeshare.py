import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}
months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']


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
    while True:
        city = input(
            "Would you like to see data for Chicago, New York City, or Washington?:\n> ").lower()
        if city in CITY_DATA:
            break
        print("Invalid city entered, please type (Chicago, New York City or Washington)\n")

    month = 'all'
    day = 'all'
    # get user input for date filter option (month, day, all)
    while True:
        filter_type = input(
            "Would you like to filter the data by month, day, or not at all?\n> ").lower()
        if filter_type in ('month', 'day', 'all', 'not at all'):
            if filter_type == 'not at all':
                filter_type = 'all'
            break

    # get user input for month (all, january, february, ... , june)
    if filter_type == 'month':
        while True:
            month = input(
                "Which month - January, February, March, April, May, or June?:\n> ").lower()
            if month in months:
                break
            print("Invalid month entered, please type (january - june) or type all\n")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    if filter_type == 'day':
        days = ['all', 'monday', 'tuesday', 'wednesday',
                'thursday', 'firday', 'saturday', 'sunday']
        while True:
            day = input(
                "Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?:\n> ").lower()
            if day in days:
                break
            print(
                "Invalid weekday entered, please type a weekday (monday - sunday) or type all\n")

    print('-'*40)
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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month)
        # filter by month to create the new dataframe
        df = df[df['month'] == month]
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    return df


def time_stats(df):
    """
    Displays statistics on the most frequent times of travel.


    Args:
        df - Pandas DataFrame containing city data used for statistical analysis
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print('Most common month:       {}.'.format(
        months[df['month'].mode()[0]].title()))

    # display the most common day of week
    print('Most common day of week: {}.'.format(df['day_of_week'].mode()[0]))

    # display the most common start hour
    print('Most common start hour:  {}.'.format(df['hour'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """
    Displays statistics on the most popular stations and trip.

    Args:
        df - Pandas DataFrame containing city data used for statistical analysis
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_stations = df['Start Station'].value_counts()
    print("\n Most commonly used Start Station: {}, with {} starts.".format(
        start_stations.index[0], start_stations[0]))

    # display most commonly used end station
    end_stations = df['End Station'].value_counts()
    print("\n Most commonly used End Station: {}, with {} ends.".format(
        end_stations.index[0], end_stations[0]))

    # display most frequent combination of start station and end station trip
    start_end_stations = df[['Start Station', 'End Station']].value_counts()
    print("\n Most commonly used Start - End Station Combination: {} -> {}, with {} combinations."
          .format(start_end_stations.index[0][0], start_end_stations.index[0][0], start_end_stations[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip duration.

    Args:
        df - Pandas DataFrame containing city data used for statistical analysis
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("Total travel time:        {:7.2f} hours.".format(
        df['Trip Duration'].sum()/60/60))

    # display mean travel time
    print("Average trip travel time: {:7.2f} minutes.".format(
        df['Trip Duration'].mean()/60))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """
    Displays statistics on bikeshare users.

    Args:
        df - Pandas DataFrame containing city data used for statistical analysis
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("\n{:<11}: {:>6}".format("User type", "Count"))
    for usertype, count in df.groupby(['User Type'])['User Type'].count().items():
        print("{:<11}: {:>6}".format(usertype, count))

    # Display counts of gender
    if 'Gender' in df.keys():
        print("\n{:<11}: {:>6}".format("Gender", "Count"))
        for gender, count in df.groupby(['Gender'])['Gender'].count().items():
            print("{:<11}: {:>6}".format(gender, count))

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.keys():
        print("\nEarlisest year of birth:   {}".format(
            int(df['Birth Year'].min())))
        print("Latest year of birth:      {}".format(
            int(df['Birth Year'].max())))
        print("Most common year of birth: {}".format(
            int(df['Birth Year'].mode()[0])))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def print_raw_data(df):
    """Displays the raw data of the filtered bikeshare data, by 5 rows each

    Args:
        df - Pandas DataFrame containing city data used for statistical analysis
    """

    # main loop to display 5 rows of the bikeshare data each
    for index in range(0, len(df), 5):
        print(df[index:index+5])
        # get user input if more data should be displayed with "yes" as default,
        # so the user can flip throguh the content by simply hitting enter
        if input('Would you like to see the next 5 lines of raw data? Enter yes or no.\n> ').lower() == 'no':
            break


def main():
    """The main loop of the bikeshare program"""
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        # get user input if raw data should be shown (yes or no with default: no)
        if input('\nWould you like to see the raw data? Enter yes or no.\n> ').lower() == 'yes':
            print_raw_data(df)

        # get user input if the program should restart or stop (default: no)
        restart = input('\nWould you like to restart? Enter yes or no.\n>')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
