import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS = ["january","february", "march", "april",\
          "may","june","all"]

DAYS = ["monday","tuesday","wednesday","thursday",\
        "friday","saturday","sunday","all"]

def get_user_input(input_variable, allowed_inputs):
    """
    Asks user to specify an input_variable
    among the list of allowed_inputs.
    
    Returns:
        (str) variable - value of the variable
    """
    # Enter again flag
    enter_again = False
    keep_asking = True
    while keep_asking or enter_again:
        print("Enter variable - {}".format(input_variable))
        print("Allowed values are - \n\t{}".format("\n\t".join(allowed_inputs)))
        # Take user input
        variable = input()
        # Remove whitespace and change to lower case
        variable = variable.strip().lower()
        # Check if variable is in allowed_inputs
        if variable in allowed_inputs:
            enter_again = False
            print("You selected: {} = {}".format(input_variable, variable))
            choice_enter_again = input("Do you want to continue with this choice? Press y or Y to confirm. Press any other key to enter new value\n").strip().lower()
            if choice_enter_again != "" and choice_enter_again[0]=='y':
                keep_asking = False
            else:
                keep_asking = True
                enter_again = True
        else:
            print("Invalid input. Try again.")
    return variable

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = get_user_input("City", CITY_DATA.keys())

    # TO DO: get user input for month (all, january, february, ... , june)
    month = get_user_input("Month", MONTHS)


    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = get_user_input("Weekday", DAYS)

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
        df - pandas DataFrame containing city data filtered by month and day
    """
    
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)+1
    
        # filter by month to create the new dataframe
        df = df[df['month']==month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week']==day.title()]
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Convert 'Start Time' to the datetime datatype
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # TO DO: display the most common month
    most_common_month = df['month'].mode().values[0]

    # TO DO: display the most common day of week
    most_common_weekday = df['day_of_week'].mode().values[0]

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_common_hour = df['hour'].mode().values[0]

    print("\tMost common month: {}".format(most_common_month))
    print("\tMost common weekday: {}".format(most_common_weekday))
    print("\tMost common hour: {}".format(most_common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print("\tMost commonly used start station: {}".format(df['Start Station'].mode().values[0]))


    # TO DO: display most commonly used end station
    print("\tMost commonly used end station: {}".format(df['End Station'].mode().values[0]))


    # TO DO: display most frequent combination of start station and end station trip
    df['Start End Stations'] = df['Start Station'] + "," + df['End Station']
    print("\tMost frequent combination of start station and end station trip: {}".format(df['Start End Stations'].mode().values[0]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    print("\tTotal travel time in seconds = {}".format(df['Trip Duration'].sum()))

    # TO DO: display mean travel time
    print("\tMean travel time in seconds = {}".format(df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print("Counts of user types\n")
    print(df['User Type'].value_counts())

    try:
        print("Printing Gender and Birth Year statistics...\n")
        # TO DO: Display counts of gender
        print(df['Gender'].value_counts())

        # TO DO: Display earliest, most recent, and most common year of birth
        print("\nEarlier year of birth: {}".format(int(df['Birth Year'].min())))
        print("\nMost recent year of birth: {}".format(int(df['Birth Year'].max())))
        print("\nMost common year of birth: {}".format(int(df['Birth Year'].mode().values[0])))
    
    except KeyError:
        print("Gender and Birth Year data is not available for the selected city.")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def show_data(df):
    """Displays data to user"""
    start_index = 0
    while True:
        view_data = input("Would you like to see the data? Press y or Y for yes. Press any other key to skip.\n")
        view_data = view_data.strip().lower()
        if view_data != "" and view_data[0] == 'y':
            print("Displaying 5 lines of data...")
            print(df[start_index:start_index+5])
            start_index+=5
        else:
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        show_data(df)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
