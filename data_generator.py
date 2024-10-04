
"""
holds the original DBs paths and function to execute a query on them.
to use it, the python file must be in the same directory as the
`Airlines_Airports_Cancellation_Codes_Flights` folder, in which the 4 csv files
are located (the big data).
"""

import duckdb
import sqlite3
import os

DB_DIR_NAME = 'Databases'

class DBsPaths:
    """
    paths to the 4 databases.
    """
    AIRLINES = 'Airlines_Airports_Cancellation_Codes_Flights/airlines.csv'
    AIRPORTS = 'Airlines_Airports_Cancellation_Codes_Flights/airports.csv'
    CANCELLATION_CODES = 'Airlines_Airports_Cancellation_Codes_Flights/cancellation_codes.csv'
    FLIGHTS = 'Airlines_Airports_Cancellation_Codes_Flights/flights.csv'

def execute_query(db_name: str, table_name: str, query: str):
    """
    queries on the 4 csv databases in the `Airlines_Airports_Cancellation_Codes_Flights` folder.\n
    create a new db if it doesn't exist and saves the `table_name` as a new table.\n
    creates a `Databases` folder if it doesn't exist, there all the db will be stored.
    :param db_name: name of the database to create or add a table to
    :param table_name: name of the new table
    :param query: the query to execute
    """

    # create a folder to store the result db of the query
    if not os.path.exists(DB_DIR_NAME):
        os.makedirs(DB_DIR_NAME)

    # create a new db if it doesn't exist
    sqlite_conn = sqlite3.connect(db_name)
    sqlite_cursor = sqlite_conn.cursor()

    try:
        query_result = duckdb.execute(query)
    except duckdb.IOException as e:
        # Include the original error message for more context
        raise duckdb.IOException('\nThe folder `Airlines_Airports_Cancellation_Codes_Flights` '
                                 'with the 4 csv files:\n'
                                 '  - flights.csv\n'
                                 '  - airports.csv\n'
                                 '  - cancellation_codes.csv\n'
                                 '  - airlines.csv\n'
                                 'is not in the same directory.\n'
                                 f'Original error: {str(e)}\n')

    # key: column name, value: column dtype
    query_result_columns_dtypes = dict(zip((col[0] for col in query_result.description),
                                           (col[1] for col in query_result.description)))

    columns_str = ', '.join([f"{col_name} {col_dtype}"
                             for col_name, col_dtype in query_result_columns_dtypes.items()])

    # delete table if exists
    sqlite_cursor.execute(f'DROP TABLE IF EXISTS {table_name}')

    # create a new table with schema as the query result
    # each column will have the appropriate dtype
    create_table_query = f"CREATE TABLE {table_name} ({columns_str})"
    sqlite_cursor.execute(create_table_query)

    # add query result's rows into new table,
    insert_query = (f"INSERT INTO {table_name} "
                    f"({', '.join(query_result_columns_dtypes.keys())}) VALUES "
                    f"({', '.join(['?'] * len(query_result_columns_dtypes))})")
    sqlite_cursor.executemany(insert_query, query_result.fetchall())

    # Commit and close
    sqlite_conn.commit()
    sqlite_cursor.close()
    sqlite_conn.close()