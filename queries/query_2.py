
from data_generator import execute_query, DBsPaths

import duckdb

DB_NAME = '..\Databases\query_2_results.db'

MONTHS = dict(zip(
    range(1, 13),
    ('january', 'february', 'march', 'april', 'may', 'june',
     'july', 'august', 'september', 'october', 'november', 'december')))

duckdb_conn = duckdb.connect()

# airports names with cancellation reason for each flight
query = f"""
SELECT airports.AIRPORT, flights.CANCELLATION_REASON, flights.MONTH
FROM '{DBsPaths.FLIGHTS}' AS flights
JOIN '{DBsPaths.AIRPORTS}' AS airports
    ON flights.ORIGIN_AIRPORT = airports.IATA_CODE
"""

airports_cancellation_reason = duckdb_conn.execute(query).df()

for i, month in MONTHS.items():
    query = f"""
    SELECT t1.AIRPORT, 100.0 * COUNT(*) / 
                                    (
                                     SELECT COUNT(*)
                                     FROM airports_cancellation_reason AS t2
                                     WHERE t1.AIRPORT = t2.AIRPORT AND t2.MONTH = {i}
                                    )  AS "cancelled_percent"
                                            
    FROM airports_cancellation_reason AS t1
    WHERE t1.CANCELLATION_REASON IS NOT NULL AND t1.MONTH = {i}
    GROUP BY t1.AIRPORT
    ORDER BY cancelled_percent DESC, t1.AIRPORT
    LIMIT 10
    """

    execute_query(DB_NAME, f'cancelled_flights_percent_{month}', query)
