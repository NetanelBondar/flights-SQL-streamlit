"""
shows the dashboard using streamlit.
to work properly, the folder `Databases` with the small dbs needs to be in the same directory
"""

import datetime
import seaborn
import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

DB_DIR_NAME = 'Databases'

FORMATTED_DAY_PERIODS = ('00:00 - 03:59', '04:00 - 07:59', '08:00 - 11:59',
                         '12:00 - 15:59', '16:00 - 19:59', '20:00 - 23:59')

# (('0000', '0359'), ('0400', '0759'), ...)
DAY_PERIODS = list(map(lambda x: x.split(' - '), FORMATTED_DAY_PERIODS))
DAY_PERIODS = tuple([(start.replace(':', ''), finish.replace(':', '')) for start, finish in DAY_PERIODS])

MONTHS_SELECTION = ('', 'January', 'February', 'March', 'April', 'May', 'June',
                    'July', 'August', 'September', 'October', 'November', 'December')

MOST_POPULAR_CONNECTIONS = ('Los Angeles International Airport', 'San Francisco International Airport',
                            'John F. Kennedy International Airport', "Chicago O'Hare International Airport",
                            'McCarran International Airport', 'LaGuardia Airport (Marine Air Terminal)')

SQLITE_ALL_AIRPORTS_CONN = sqlite3.connect(f'{DB_DIR_NAME}/all_airports.db')
SQLITE_ORIGINAL_CONN = sqlite3.connect(f'{DB_DIR_NAME}/sample_original.db')
SQLITE_1_CONN = sqlite3.connect(f'{DB_DIR_NAME}/query_1_results.db')
SQLITE_2_CONN = sqlite3.connect(f'{DB_DIR_NAME}/query_2_results.db')
SQLITE_3_CONN = sqlite3.connect(f'{DB_DIR_NAME}/query_3_results.db')
SQLITE_4_CONN = sqlite3.connect(f'{DB_DIR_NAME}/query_4_results.db')
SQLITE_SPARK_QUERY_CONN = sqlite3.connect(f'{DB_DIR_NAME}/flight_analysis.db')


def str_vals_to_int(str_vals: str) -> int | list[int]:
    """
    converts string values seperated by comma to list of integers
    :param str_vals: string values seperated by comma
    :return: list of integers
    """
    # sometimes we get a single number
    if isinstance(str_vals, int):
        return str_vals

    return list(map(int, str_vals.split(',')))


def clean_airline_str(airline_str: str) -> str:
    """
    removes unnecessary repeated words from airline names like 'Airline' etc.
    :param airline_str: name of an airline
    :return: the same name without the unnecessary repeated words
    """
    return (airline_str.replace('Airlines', '').
            replace('Inc.', '').replace('Air', '').
            replace('Lines', '').strip())


def clean_airport_str(airport_str: str) -> str:
    """
    removes unnecessary repeated words from airport names like 'Airport' etc.
    :param airport_str: name of an airport
    :return: the same name without the unnecessary repeated words
    """
    return airport_str.replace('Airport ', '').replace('Airport', '').strip()


def get_all_airports() -> tuple[str]:
    """
    :return: all airports in the database
    """

    result_better = pd.read_sql_query('SELECT * FROM all_airports_table', SQLITE_ALL_AIRPORTS_CONN)

    result_better = tuple([value[0] for value in result_better.values])

    return result_better


def show_sample_original():
    """
    shows in the streamlit page samples tables from the 4 original databases.
    the columns we used are marked
    """
    result_airlines = pd.read_sql_query(f'SELECT * FROM airlines_sample',
                                        SQLITE_ORIGINAL_CONN)
    result_airports = pd.read_sql_query(f'SELECT * FROM airports_sample',
                                        SQLITE_ORIGINAL_CONN)
    result_cancellation_codes = pd.read_sql_query(f'SELECT * FROM cancellation_codes_sample',
                                                  SQLITE_ORIGINAL_CONN)
    result_flights = pd.read_sql_query(f'SELECT * FROM flights_sample',
                                       SQLITE_ORIGINAL_CONN)

    st.title('Original Data (columns we processed are marked)')
    st.text('Airlines Table')
    st.dataframe(result_airlines.style.
                 set_properties(**{'background-color': '#BA494B'},
                                subset=['AIRLINE']))
    st.text('Airports Table')
    st.dataframe(result_airports.style.
                 set_properties(**{'background-color': '#BA494B'},
                                subset=['AIRPORT']))
    st.text('Cancellation Description Table')
    st.dataframe(result_cancellation_codes.style.
                 set_properties(**{'background-color': '#BA494B'},
                                subset=['CANCELLATION_DESCRIPTION']))
    st.text('Flights Table')
    st.dataframe(result_flights.style.
                 set_properties(**{'background-color': '#BA494B'},
                                subset=['MONTH', 'DAY', 'SCHEDULED_DEPARTURE',
                                        'DEPARTURE_DELAY', 'ARRIVAL_DELAY',
                                        'CANCELLATION_REASON', 'DISTANCE']))


def show_graph_1():
    """
    shows the first graph in the streamlit page.
    asks for a period of the day and shows a box plot of departure delays for
    each airline in that period of day.
    """
    st.title("Delays Relative to Airlines and Time of the Day")

    selected_option = st.radio('Choose a time to see how much the airlines are delayed:',
                               [''] + list(FORMATTED_DAY_PERIODS), index=None)

    st.text('We can see that some the most reliable airlines are: Delta and Hawaiian.')
    st.text('Some of the most unreliable airlines are: Spirit, Frontier and American Eagle.')

    if selected_option is None or selected_option == '':
        return

    for span_index, option in enumerate(FORMATTED_DAY_PERIODS):
        if selected_option == option:
            break

    # read the data from the appropriate first query table
    result = pd.read_sql_query(f'SELECT * FROM bet_{DAY_PERIODS[span_index][0]}_to_{DAY_PERIODS[span_index][1]}',
                               SQLITE_1_CONN)

    # extract the columns
    airlines, delays = ([values[0] for values in result.values],
                        [values[1] for values in result.values])

    airlines = list(map(clean_airline_str, airlines))

    delays = list(map(str_vals_to_int, delays))

    positions = range(1, len(airlines) + 1)

    fig, ax = plt.subplots()

    ax.boxplot(delays, flierprops=dict(marker='_'))

    ax.set_xticks(ticks=positions, labels=airlines, rotation=20, ha='right')

    ax.set_title(f'Delay Time {FORMATTED_DAY_PERIODS[span_index]}')
    ax.set_ylabel('Delay (m)')
    ax.set_xlabel('Airline')
    plt.tight_layout()

    st.pyplot(fig)


def show_graph_2():
    """
    shows the second graph in the streamlit page.
    asks for month(s) and shows a pie chart of the top 10 cancellation
    flight airports for each month selected.
    """
    st.title('Top 10 Cancelled Flights Percentage Airports Based on Month')

    months_selected = st.multiselect('Choose month(s) to see the '
                                     'top cancelled fights percentage airports', MONTHS_SELECTION)

    if months_selected is None or len(months_selected) == 0:
        return

    for selected_month in months_selected:
        result = pd.read_sql_query(f'SELECT * FROM cancelled_flights_percent_{selected_month}', SQLITE_2_CONN)

        airports, cancel_percents = ([values[0] for values in result.values],
                                     [values[1] for values in result.values])

        airports = list(map(clean_airport_str, airports))

        fig, ax = plt.subplots(figsize=(10, 6))

        ax.pie(cancel_percents, startangle=140, autopct='%1.1f%%', textprops={'fontsize': 15})

        ax.axis('equal')

        ax.set_title(f'Cancellation Percentage {selected_month.capitalize()}', fontsize=15)

        plt.subplots_adjust(left=0.0, bottom=0.1, right=0.45)

        ax.legend(airports, title="Airports", bbox_to_anchor=(1, 0.5))

        st.pyplot(fig)


def show_graph_3():
    """
    shows the third graph in the streamlit page.
    asks for the origin airport, destination airport, and date of flight.
    shows a scatter plot with X being the departure delay and Y being the arrival delay.
    in addition, each dot is colored according to the period of day the flight was scheduled.
    """
    all_airports = get_all_airports()

    st.title("How Does Departure Delay Affect Arrival Delay? Based on Origin & Destination Airports and Month")

    st.text(f'Most Popular Airports Connections:\n' + '\n'.join(MOST_POPULAR_CONNECTIONS))

    origin = st.multiselect('Choose origin airport',
                            all_airports,
                            max_selections=1)

    destination = st.multiselect('Choose destination airport',
                                 all_airports,
                                 max_selections=1)

    d = st.date_input("What date is your flight",
                      min_value=datetime.date(2015, 1, 1),
                      max_value=datetime.date(2015, 12, 31),
                      value=None)

    if (origin is None or len(origin) == 0 or destination is None or
            len(destination) == 0 or d is None):
        return

    origin = origin[0]
    destination = destination[0]

    # query to extract the departure and arrival delay and scheduled departure
    # for flights in the selected connection and date with max delay of 60 minutes
    query = f"""
SELECT DEPARTURE_DELAY, ARRIVAL_DELAY, SCHEDULED_DEPARTURE
FROM departure_vs_arrival_delay 
WHERE origin = "{origin}" AND destination = "{destination}" AND 
      DEPARTURE_DELAY BETWEEN 0 AND 60
      AND MONTH = {d.month} AND DAY = {d.day}
"""

    result = pd.read_sql_query(query, SQLITE_3_CONN)

    if len(result.values) == 0:
        st.text("There is no flights data")
        return

    dep_delays, arriv_delays, sche_deps = ([values[0] for values in result.values],
                                           [values[1] for values in result.values],
                                           [values[2] for values in result.values])

    # 3 -> 0003, 14 -> 0014, 148 -> 0148, 1236 -> 1236
    sche_deps = list(map(lambda x: '0' * (4 - len(str(x))) + str(x), sche_deps))

    # for each scheduled flight time assign a day period label.
    # for example, 0715 is given the label '04:00 - 07:59'
    day_period_labels = []
    for sche_dep in sche_deps:
        for i, day_period in enumerate(DAY_PERIODS):
            if sche_dep <= day_period[1]:
                day_period_labels.append(FORMATTED_DAY_PERIODS[i])
                break

    df = pd.DataFrame({'departure_delay': dep_delays, 'arrival_delay': arriv_delays,
                       'scheduled_departure': sche_deps, 'time': day_period_labels})

    fig, ax = plt.subplots()

    seaborn.scatterplot(data=df, x='departure_delay', y='arrival_delay', hue='time')

    seaborn.lineplot(x=(0, 60), y=(0, 60), color='black', alpha=0.5)

    plt.xlim(-5, 60)
    plt.ylim(-25, 60)

    st.text("If the point is below the black line,\n"
            "the departure delay didn't affect the arrival delay that much.")
    st.text("If the point is above the black line,\n"
            "the departure delay maybe was the reason for the arrival delay to be even worse.")
    st.text("If the point is on the black line,\n"
            "the arrival delay was the same as the departure delay.")

    st.pyplot(fig)


def show_graph_4():
    """
    shows the fourth graph in the streamlit page.
    asks for a month.
    shows a pie chart of percentages of cancellation reasons for each month.
    """
    st.title("Percentage for each Cancellation Reason Based on Month")

    selected_month = st.radio('Choose month', MONTHS_SELECTION)

    if selected_month is None or selected_month == '':
        return

    result = pd.read_sql_query(f'SELECT * FROM cancellation_reason_percentage_{selected_month.lower()}', SQLITE_4_CONN)

    cancellation_reasons, percents = ([values[0] for values in result.values],
                                      [values[1] for values in result.values])

    fig, ax = plt.subplots()

    color_mapping = {
        'National Air System': 'red',
        'Weather': 'blue',
        'Airline/Carrier': 'green',
        'Security': 'purple'
    }

    colors = [color_mapping[cancellation_reason] for cancellation_reason in cancellation_reasons]

    ax.pie(percents, labels=cancellation_reasons, autopct='%1.1f%%', colors=colors)

    ax.axis('equal')
    ax.set_title("Cancellation Reason Percentage")

    st.text("We can see that during the summer months the Weather doesn't effect cancellation"
            "as much as the rest of the year.")

    st.pyplot(fig)


def show_spark_query_graph():
    st.title("Average Distance for each Airline (Spark Query)")

    result = pd.read_sql_query(f'SELECT * FROM "average_distance"', SQLITE_SPARK_QUERY_CONN)

    airline, avg_distance = ([values[0] for values in result.values],
                             [values[1] for values in result.values])

    fig, ax = plt.subplots()

    ax.bar(airline, avg_distance)

    ax.set_title("Average Distance for each Airline")
    ax.set_xlabel("Airline")
    ax.set_ylabel("Average Distance (miles)")

    st.pyplot(fig)


show_sample_original()
show_graph_1()
show_graph_2()
show_graph_3()
show_graph_4()
show_spark_query_graph()
