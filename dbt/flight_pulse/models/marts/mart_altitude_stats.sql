WITH base AS (
    SELECT * FROM {{ ref('int_flights_cleaned') }}
)

SELECT
    origin_country,
    altitude_band,
    count(*) AS total_flights,
    round(min(altitude)::NUMERIC, 2) AS min_altitude,
    round(max(altitude)::NUMERIC, 2) AS max_altitude,
    round(avg(altitude)::NUMERIC, 2) AS avg_altitude
FROM base
GROUP BY origin_country, altitude_band
ORDER BY origin_country, altitude_band