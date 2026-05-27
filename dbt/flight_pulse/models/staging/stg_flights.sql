WITH source AS (
    SELECT * FROM flights_raw
),

renamed AS (
    SELECT
        id,
        trim(icao24) AS icao24,
        trim(callsign) AS callsign,
        origin_country,
        longitude,
        latitude,
        altitude,
        velocity,
        to_timestamp(TIMESTAMP) AS flight_timestamp,
        date_trunc('hour', to_timestamp(TIMESTAMP)) AS flight_hour,
        ingested_at
    FROM source
    WHERE callsign IS NOT NULL
      AND longitude IS NOT NULL
      AND latitude IS NOT NULL
      AND trim(callsign) != ''
)

SELECT * FROM renamed