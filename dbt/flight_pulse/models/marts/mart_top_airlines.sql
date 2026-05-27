WITH base AS (
    SELECT * FROM {{ ref('int_flights_cleaned') }}
)

SELECT
    callsign,
    origin_country,
    count(*) AS total_flights,
    round(avg(altitude)::NUMERIC, 2) AS avg_altitude,
    round(avg(velocity)::NUMERIC, 2) AS avg_velocity
FROM base
GROUP BY callsign, origin_country
ORDER BY total_flights DESC
LIMIT 15