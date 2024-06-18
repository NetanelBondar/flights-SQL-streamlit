
import duckdb
import sqlite3

class DBsPaths:
    """paths to the 4 databases"""
    AIRLINES = 'Airlines_Airports_Cancellation_Codes_Flights/airlines.csv'
    AIRPORTS = 'Airlines_Airports_Cancellation_Codes_Flights/airports.csv'
    CANCELLATION_CODES = 'Airlines_Airports_Cancellation_Codes_Flights/cancellation_codes.csv'
    FLIGHTS = 'Airlines_Airports_Cancellation_Codes_Flights/flights.csv'

class DataGenerator:
    """
    creates a new db if it's not exists.\n
    then, can execute queries on the 4 csv files and save the results as tables
    in the db.
    :param db_name: name of the database to create or add a table to
    """
    def __init__(self, db_name: str):

        self.sqlite_conn = sqlite3.connect(db_name)
        self.sqlite_cursor = self.sqlite_conn.cursor()

    def query(self, table_name: str, query: str):
        """
        Queries the database and saves the result as a new table
        :param table_name: name of the new table
        :param query: the query to execute
        """

        query_result = duckdb.execute(query)

        # key: column name, value: column dtype
        query_result_columns_dtypes = dict(zip((col[0] for col in query_result.description),
                                               (col[1] for col in query_result.description)))

        columns_str = ', '.join([f"{col_name} {col_dtype}"
                                 for col_name, col_dtype in query_result_columns_dtypes.items()])

        # delete table if exists
        self.sqlite_cursor.execute(f'DROP TABLE IF EXISTS {table_name}')

        # create new table with schema as the query result
        create_table_query = f"CREATE TABLE {table_name} ({columns_str})"
        self.sqlite_cursor.execute(create_table_query)

        # add query result's rows into new table
        insert_query = (f"INSERT INTO {table_name} "
                        f"({', '.join(query_result_columns_dtypes.keys())}) VALUES "
                        f"({', '.join(['?'] * len(query_result_columns_dtypes))})")
        self.sqlite_cursor.executemany(insert_query, query_result.fetchall())

        # Commit and close
        self.sqlite_conn.commit()
        self.sqlite_cursor.close()
        self.sqlite_conn.close()