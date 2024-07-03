"""
queries the big data to answer question 5
"""

from data_generator import execute_query, DBsPaths, DB_DIR_NAME

DB_NAME = 'query_5_results.db'


query = f"""
SELECT flights.DAY_OF_WEEK, SUM(flights.DISTANCE) AS SumDistance
FROM '{DBsPaths.FLIGHTS}' AS flights
GROUP BY flights.DAY_OF_WEEK
"""

execute_query(f'{DB_DIR_NAME}/{DB_NAME}', f'distance_by_week_day', query)