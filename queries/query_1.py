
from data_generator import execute_query, DBsPaths, DB_DIR_PATH

SPANS = (('0000', '0359'), ('0400', '0759'), ('0800', '1159'),
         ('1200', '1559'), ('1600', '1959'), ('2000', '2359'))


DB_NAME = f'{DB_DIR_PATH}/query_1_results.db'

for span in SPANS:

    query = f"""
    SELECT airlines.AIRLINE, GROUP_CONCAT(flights.DEPARTURE_DELAY) AS "departure_delay",
    FROM '{DBsPaths.FLIGHTS}' AS flights
    JOIN '{DBsPaths.AIRLINES}' AS airlines
        ON flights.AIRLINE = airlines.IATA_CODE
    WHERE flights.DEPARTURE_DELAY BETWEEN 0 AND 120 AND flights.SCHEDULED_DEPARTURE
                                            BETWEEN '{span[0]}' AND '{span[1]}'
    GROUP BY airlines.AIRLINE
    ORDER BY airlines.AIRLINE
    """

    execute_query(DB_NAME, f'bet_{span[0]}_to_{span[1]}', query)


