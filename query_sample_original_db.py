
"""
generate the data for sample data from each csv file
"""

from data_generator import execute_query, DBsPaths, DB_DIR_NAME

DB_NAME = 'sample_original.db'

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

execute_query(f'{DB_DIR_NAME}/{DB_NAME}', 'airports_sample', query_airports)
execute_query(f'{DB_DIR_NAME}/{DB_NAME}', 'airlines_sample', query_airlines)
execute_query(f'{DB_DIR_NAME}/{DB_NAME}', 'cancellation_codes_sample', query_cancellation_codes)
execute_query(f'{DB_DIR_NAME}/{DB_NAME}', 'flights_sample', query_flights)




