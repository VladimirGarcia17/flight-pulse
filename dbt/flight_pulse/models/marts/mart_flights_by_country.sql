WITH base AS (
    SELECT * FROM {{ ref('int_flights_cleaned') }}
)

SELECT
    origin_country,
    count(*) AS total_flights,
    round(avg(altitude)::NUMERIC, 2) AS avg_altitude,
    round(avg(velocity)::NUMERIC, 2) AS avg_velocity
FROM base
GROUP BY origin_country
ORDER BY total_flights DESC