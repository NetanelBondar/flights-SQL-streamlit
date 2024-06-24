
import duckdb
import sqlite3
import os

DB_DIR_PATH = '../Databases'

class DBsPaths:
    """
    paths to the 4 databases.
    assumes the `Airlines_Airports_Cancellation_Codes_Flights` folder exists
    in the same directory
    """
    AIRLINES = 'Airlines_Airports_Cancellation_Codes_Flights/airlines.csv'
    AIRPORTS = 'Airlines_Airports_Cancellation_Codes_Flights/airports.csv'
    CANCELLATION_CODES = 'Airlines_Airports_Cancellation_Codes_Flights/cancellation_codes.csv'
    FLIGHTS = 'Airlines_Airports_Cancellation_Codes_Flights/flights.csv'

def execute_query(db_name: str, table_name: str, query: str):
    """
    create a new db if it doesn't exist.\n
    queries the database and saves the airports_cancellation_reason as a new table.
    :param db_name: name of the database to create or add a table to
    :param table_name: name of the new table
    :param query: the query to execute
    """

    if not os.path.exists(DB_DIR_PATH):
        os.makedirs(DB_DIR_PATH)

    sqlite_conn = sqlite3.connect(db_name)
    sqlite_cursor = sqlite_conn.cursor()

    query_result = duckdb.execute(query)

    # key: column name, value: column dtype
    query_result_columns_dtypes = dict(zip((col[0] for col in query_result.description),
                                           (col[1] for col in query_result.description)))

    columns_str = ', '.join([f"{col_name} {col_dtype}"
                             for col_name, col_dtype in query_result_columns_dtypes.items()])

    # delete table if exists
    sqlite_cursor.execute(f'DROP TABLE IF EXISTS {table_name}')

    # create new table with schema as the query airports_cancellation_reason
    # each column will have the appropriate dtype
    create_table_query = f"CREATE TABLE {table_name} ({columns_str})"
    sqlite_cursor.execute(create_table_query)

    # add query airports_cancellation_reason's rows into new table,
    insert_query = (f"INSERT INTO {table_name} "
                    f"({', '.join(query_result_columns_dtypes.keys())}) VALUES "
                    f"({', '.join(['?'] * len(query_result_columns_dtypes))})")
    sqlite_cursor.executemany(insert_query, query_result.fetchall())

    # Commit and close
    sqlite_conn.commit()
    sqlite_cursor.close()
    sqlite_conn.close()