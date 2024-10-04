
"""
generate the data to get all the airports
"""

from data_generator import execute_query, DBsPaths, DB_DIR_NAME

DB_NAME = f'all_airports.db'

query = f"""
SELECT AIRPORT
FROM '{DBsPaths.AIRPORTS}'
"""

execute_query(f'{DB_DIR_NAME}/{DB_NAME}', 'all_airports_table', query)




