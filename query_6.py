"""
queries the big data to answer question 6
"""

from data_generator import execute_query, DBsPaths, DB_DIR_NAME

SPANS = (('0000', '0359'), ('0400', '0759'), ('0800', '1159'),
         ('1200', '1559'), ('1600', '1959'), ('2000', '2359'))


DB_NAME = 'query_6_results.db'

query = f"""
SELECT 
    flights.DESTINATION_AIRPORT, 
    SUM(CASE 
            WHEN SUBSTR(flights.SCHEDULED_DEPARTURE, 1, 4) BETWEEN '{SPANS[0][0]}' AND '{SPANS[0][1]}' THEN flights.TAXI_OUT 
            ELSE 0 
        END) AS TaxiOut_0000_0359,
    SUM(CASE 
            WHEN SUBSTR(flights.SCHEDULED_DEPARTURE, 1, 4) BETWEEN '{SPANS[1][0]}' AND '{SPANS[1][1]}' THEN flights.TAXI_OUT 
            ELSE 0 
        END) AS TaxiOut_0400_0759,
    SUM(CASE 
            WHEN SUBSTR(flights.SCHEDULED_DEPARTURE, 1, 4) BETWEEN '{SPANS[2][0]}' AND '{SPANS[2][1]}' THEN flights.TAXI_OUT 
            ELSE 0 
        END) AS TaxiOut_0800_1159,
    SUM(CASE 
            WHEN SUBSTR(flights.SCHEDULED_DEPARTURE, 1, 4) BETWEEN '{SPANS[3][0]}' AND '{SPANS[3][1]}' THEN flights.TAXI_OUT 
            ELSE 0 
        END) AS TaxiOut_1200_1559,
    SUM(CASE 
            WHEN SUBSTR(flights.SCHEDULED_DEPARTURE, 1, 4) BETWEEN '{SPANS[4][0]}' AND '{SPANS[4][1]}' THEN flights.TAXI_OUT 
            ELSE 0 
        END) AS TaxiOut_1600_1959,
    SUM(CASE 
            WHEN SUBSTR(flights.SCHEDULED_DEPARTURE, 1, 4) BETWEEN '{SPANS[5][0]}' AND '{SPANS[5][1]}' THEN flights.TAXI_OUT 
            ELSE 0 
        END) AS TaxiOut_2000_2359
FROM '{DBsPaths.FLIGHTS}' AS flights
GROUP BY flights.DESTINATION_AIRPORT
"""

execute_query(f'{DB_DIR_NAME}/{DB_NAME}', 'QuantityTaxiHourAirport', query)






#
# """
# queries the big data to answer question 6
# """
#
# from data_generator import execute_query, DBsPaths, DB_DIR_NAME
#
# SPANS = (('0000', '0359'), ('0400', '0759'), ('0800', '1159'),
#          ('1200', '1559'), ('1600', '1959'), ('2000', '2359'))
#
#
# DB_NAME = 'query_6_results.db'
#
# query = f"""
# SELECT flights.DESTINATION_AIRPORT, SUM(flights.TAXI_OUT) AS QuantityTaxiOut
# FROM '{DBsPaths.FLIGHTS}' AS flights
# GROUP BY flights.DESTINATION_AIRPORT
# """
#
# execute_query(f'{DB_DIR_NAME}/{DB_NAME}', f'QuantityTaxiHourAirport', query)
