

from data_generator import DataGenerator, DBsPaths

query = f"""
SELECT TAIL_NUMBER, flights.SCHEDULED_DEPARTURE, flights.DAY, cancellations.CANCELLATION_DESCRIPTION
FROM '{DBsPaths.FLIGHTS}' AS flights
JOIN '{DBsPaths.CANCELLATION_CODES}' AS cancellations
    ON flights.CANCELLATION_REASON = cancellations.CANCELLATION_REASON
"""

dbGenerator = DataGenerator('results.db')

dbGenerator.query('tail_time_day_reason_cancelled_flights', query)