

from data_generator import execute_query, DBsPaths, DB_DIR_NAME

SPANS = (('0000', '0359'), ('0400', '0759'), ('0800', '1159'),
         ('1200', '1559'), ('1600', '1959'), ('2000', '2359'))


DB_NAME = 'query_6_results.db'

query = f"""
SELECT airlines.AIRLINE, SUM(flights.AIR_TIME) / 60 AS SUM_AIRTIME
FROM '{DBsPaths.FLIGHTS}' AS flights
JOIN '{DBsPaths.AIRLINES}' AS airlines
    ON flights.AIRLINE = airlines.IATA_CODE
GROUP BY airlines.AIRLINE
"""

execute_query(f'{DB_DIR_NAME}/{DB_NAME}', 'sum_airtime_airlines', query)
