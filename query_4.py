
"""
generate the data for the fourth graph in the streamlit page
"""

from data_generator import execute_query, DBsPaths, DB_DIR_NAME

DB_NAME = 'query_4_results.db'

MONTHS = dict(zip(
    range(1, 13),
    ('january', 'february', 'march', 'april', 'may', 'june',
     'july', 'august', 'september', 'october', 'november', 'december')))

for i, month in MONTHS.items():
    query = f"""
    SELECT cancellation_codes.CANCELLATION_DESCRIPTION,
            100.0 * COUNT(*) / SUM(COUNT(*)) OVER () AS percentage
    
    FROM '{DBsPaths.FLIGHTS}' AS flights
    JOIN '{DBsPaths.CANCELLATION_CODES}' AS cancellation_codes
        ON flights.CANCELLATION_REASON = cancellation_codes.CANCELLATION_REASON
    WHERE flights.CANCELLATION_REASON IS NOT NULL AND MONTH = {i}
    GROUP BY cancellation_codes.CANCELLATION_DESCRIPTION
    """

    execute_query(f'{DB_DIR_NAME}/{DB_NAME}', f'cancellation_reason_percentage_{month}', query)
