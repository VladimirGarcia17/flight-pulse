WITH stg AS (
    SELECT * FROM {{ ref('stg_flights') }}
),

enriched AS (
    SELECT
        icao24,
        callsign,
        origin_country,
        longitude,
        latitude,
        altitude,
        velocity,
        flight_timestamp,
        flight_hour,
        extract(HOUR FROM flight_timestamp) AS hour_of_day,
        CASE
            WHEN altitude < 1000 THEN 'low'
            WHEN altitude < 8000 THEN 'cruise'
            ELSE 'high'
        END AS altitude_band,
        CASE
            WHEN velocity < 100 THEN 'slow'
            WHEN velocity < 300 THEN 'medium'
            ELSE                     'fast'
        END AS speed_band
    FROM stg
    WHERE altitude > 0
      AND velocity > 0
)

SELECT * FROM enriched