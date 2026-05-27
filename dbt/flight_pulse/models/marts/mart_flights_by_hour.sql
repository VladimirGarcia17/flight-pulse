WITH base AS (
    SELECT * FROM {{ ref('int_flights_cleaned') }}
)

SELECT
    hour_of_day,
    count(*) AS total_flights,
    round(avg(altitude)::NUMERIC, 2) AS avg_altitude,
    round(avg(velocity)::NUMERIC, 2) AS avg_velocity
FROM base
GROUP BY hour_of_day
ORDER BY hour_of_day