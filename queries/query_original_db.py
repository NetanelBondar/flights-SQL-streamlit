
from data_generator import execute_query, DBsPaths

DB_NAME = '..\Databases\original_sample.db'

query_airports = f"""
SELECT *
FROM '{DBsPaths.AIRPORTS}'
LIMIT 50
"""
query_airlines = f"""
SELECT *
FROM '{DBsPaths.AIRLINES}'
LIMIT 50
"""
query_cancellation_codes = f"""
SELECT *
FROM '{DBsPaths.CANCELLATION_CODES}'
LIMIT 50
"""

row_not_null_query_flights = ' AND '.join([f'{i} IS NOT NULL' for i in range(1, 32)])

query_flights = f"""
SELECT *
FROM '{DBsPaths.FLIGHTS}'
WHERE {row_not_null_query_flights}
LIMIT 50
"""

execute_query(DB_NAME, 'airports_sample', query_airports)
execute_query(DB_NAME, 'airlines_sample', query_airlines)
execute_query(DB_NAME, 'cancellation_codes_sample', query_cancellation_codes)
execute_query(DB_NAME, 'flights_sample', query_flights)




