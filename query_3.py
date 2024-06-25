from data_generator import execute_query, DBsPaths, DB_DIR_NAME

DB_NAME = 'query_3_results.db'

query = f"""
SELECT airports_1.AIRPORT AS origin, airports_2.AIRPORT AS destination,
       flights.DEPARTURE_DELAY, flights.ARRIVAL_DELAY, flights.SCHEDULED_DEPARTURE, flights.MONTH, flights.DAY
FROM '{DBsPaths.FLIGHTS}' AS flights
JOIN '{DBsPaths.AIRPORTS}' AS airports_1
    ON flights.ORIGIN_AIRPORT = airports_1.IATA_CODE
JOIN '{DBsPaths.AIRPORTS}' AS airports_2
    ON flights.DESTINATION_AIRPORT = airports_2.IATA_CODE
WHERE flights.DEPARTURE_DELAY > 0
"""

execute_query(f'{DB_DIR_NAME}/{DB_NAME}', f'departure_vs_arrival_delay', query)
