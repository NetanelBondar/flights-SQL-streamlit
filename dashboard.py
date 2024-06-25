import datetime
import seaborn
import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

from data_generator import DB_DIR_NAME

FORMATTED_SPANS = ('00:00 - 03:59', '04:00 - 07:59', '08:00 - 11:59',
                   '12:00 - 15:59', '16:00 - 19:59', '20:00 - 23:59')

# (('0000', '0359'), ('0400', '0759'), ...)
SPANS = list(map(lambda x: x.split(' - '), FORMATTED_SPANS))
SPANS = tuple([(start.replace(':', ''), finish.replace(':', '')) for start, finish in SPANS])

MONTHS_SELECTION = ('', 'January', 'February', 'March', 'April', 'May', 'June',
                    'July', 'August', 'September', 'October', 'November', 'December')

MOST_POPULAR_CONNECTIONS = ('Los Angeles International Airport', 'San Francisco International Airport',
                            'John F. Kennedy International Airport', "Chicago O'Hare International Airport",
                            'McCarran International Airport', 'LaGuardia Airport (Marine Air Terminal)')

SQLITE_ORIGINAL_CONN = sqlite3.connect('Databases/original_sample.db')
SQLITE_1_CONN = sqlite3.connect('Databases/query_1_results.db')
SQLITE_2_CONN = sqlite3.connect('Databases/query_2_results.db')
SQLITE_3_CONN = sqlite3.connect('Databases/query_3_results.db')
SQLITE_4_CONN = sqlite3.connect('Databases/query_4_results.db')


def str_vals_to_int(str_vals):
    if isinstance(str_vals, int):
        return str_vals

    return list(map(int, str_vals.split(',')))


def clean_airline_str(airline_str):
    return (airline_str.replace('Airlines', '').
            replace('Inc.', '').replace('Air', '').
            replace('Lines', '').strip())


def clean_airport_str(airport_str):
    return airport_str.replace('Airport ', '').replace('Airport', '').strip()


def get_all_airports():
    """
    :return: all airports in the database
    """
    sqlite_conn = sqlite3.connect(f'{DB_DIR_NAME}/all_airports.db')
    sqlite_cursor = sqlite_conn.cursor()

    sqlite_cursor.execute('SELECT * FROM all_airports_table')

    result = tuple(item[0] for item in sqlite_cursor.fetchall())

    return result

def show_sample_original():

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
                 set_properties(**{'background-color': '#BA494B'}, subset=['AIRLINE']))
    st.text('Airports Table')
    st.dataframe(result_airports.style.
                 set_properties(**{'background-color': '#BA494B'}, subset=['AIRPORT']))
    st.text('Cancellation Description Table')
    st.dataframe(result_cancellation_codes.style.
                 set_properties(**{'background-color': '#BA494B'}, subset=['CANCELLATION_DESCRIPTION']))
    st.text('Flights Table')
    st.dataframe(result_flights.style.
                 set_properties(**{'background-color': '#BA494B'},
                                subset=['MONTH', 'DAY', 'SCHEDULED_DEPARTURE',
                                        'DEPARTURE_DELAY', 'ARRIVAL_DELAY', 'CANCELLATION_REASON']))


def show_graph_1():
    st.title("Delays Relative to Airlines and Time of the Day")

    selected_option = st.radio('Choose a time to see how much the airlines are delayed:',
                               [''] + list(FORMATTED_SPANS), index=None)

    st.text('We can see that some the most reliable airlines are: Delta and Hawaiian')
    st.text('Some of the most unreliable airlines are: Spirit, Frontier and American Eagle')

    if selected_option is None or selected_option == '':
        return

    for span_index, option in enumerate(FORMATTED_SPANS):
        if selected_option == option:
            break

    result = pd.read_sql_query(f'SELECT * FROM bet_{SPANS[span_index][0]}_to_{SPANS[span_index][1]}',
                               SQLITE_1_CONN)

    airlines, delays = ([values[0] for values in result.values],
                        [values[1] for values in result.values])

    airlines = list(map(clean_airline_str, airlines))

    delays = list(map(str_vals_to_int, delays))

    positions = range(1, len(airlines) + 1)

    fig, ax = plt.subplots()

    ax.boxplot(delays, flierprops=dict(marker='_'))

    ax.set_xticks(ticks=positions, labels=airlines, rotation=20, ha='right')

    ax.set_title(f'Delay Time {FORMATTED_SPANS[span_index]}')
    ax.set_ylabel('Delay (m)')
    ax.set_xlabel('Airline')
    plt.tight_layout()

    st.pyplot(fig)


def show_graph_2():
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

    all_airports = get_all_airports()

    st.title("How Does Departure Delay Affect Arrival Delay? Based on Origin & Destination Airports and Month")

    st.text(f'Most Popular Airports Connections:\n' + '\n'.join(MOST_POPULAR_CONNECTIONS))

    airports_pair = st.multiselect('Choose origin and destination airports',
                                   all_airports,
                                   max_selections=2)

    d = st.date_input("What date is your flight",
                      min_value=datetime.date(2015, 1, 1),
                      max_value=datetime.date(2015, 12, 31),
                      value=None)

    if len(airports_pair) != 2 or airports_pair[0] is None or airports_pair[1] is None:
        return

    query = f"""
SELECT DEPARTURE_DELAY, ARRIVAL_DELAY, SCHEDULED_DEPARTURE
FROM departure_vs_arrival_delay 
WHERE origin = "{airports_pair[0]}" AND destination = "{airports_pair[1]}" AND 
      DEPARTURE_DELAY BETWEEN 0 AND 120
      AND MONTH = {d.month} AND DAY = {d.day}
"""

    result = pd.read_sql_query(query, SQLITE_3_CONN)

    if len(result.values) == 0:
        st.text("There is no flights data")
        return

    dep_delays, arriv_delays, sche_deps = ([values[0] for values in result.values],
                                           [values[1] for values in result.values],
                                           [values[2] for values in result.values])

    sche_deps = list(map(int, sche_deps))
    sche_deps = list(map(lambda x: '0' * (4 - len(str(x))) + str(x), sche_deps))

    times_labels = []
    for sche_dep in sche_deps:
        for time_cat in FORMATTED_SPANS:
            time_cat_lim = time_cat[-5:].replace(':', '')
            if sche_dep <= time_cat_lim:
                times_labels.append(time_cat)
                break

    df = pd.DataFrame({'departure_delay': dep_delays, 'arrival_delay': arriv_delays,
                       'scheduled_departure': sche_deps, 'time': times_labels})

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


show_sample_original()
show_graph_1()
show_graph_2()
show_graph_3()
show_graph_4()