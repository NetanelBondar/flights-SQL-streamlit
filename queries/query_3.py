from data_generator import execute_query, DBsPaths

DB_NAME = '..\Databases\query_3_results.db'

SPANS = (('0000', '0359'), ('0400', '0759'), ('0800', '1159'),
         ('1200', '1559'), ('1600', '1959'), ('2000', '2359'))

MOST_POPULAR_CONNECTIONS = (('LAX', 'SFO'), ('SFO', 'LAX'), ('LAX', 'JFK'),
                            ('ORD', 'LAX'), ('ORD', 'SFO'), ('LAX', 'LAS'),
                            ('ORD', 'LGA'), ('LAS', 'LAX'), ('JFK', 'LAX'),
                            ('LAS', 'SFO'))

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

execute_query(DB_NAME, f'departure_vs_arrival_delay', query)
