import json
import psycopg2
from kafka import KafkaConsumer
from datetime import datetime

KAFKA_BROKER = "kafka:29092"
TOPIC = "flights-raw"

DB_CONFIG = {
    "host": 'postgres',
    "port": 5432,
    "dbname": 'flightdb',
    "user": 'flightuser',
    "password": 'flightpass'
}

# Initialize consumer
consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    value_deserializer=lambda v: json.loads(v.decode("utf-8"))
)

# Insert on PostgreSQL
def insert_flights(cursor, flights):
    query = """
        INSERT INTO flights_raw 
            (icao24, callsign, origin_country, longitude, latitude, altitude, velocity, timestamp)
        VALUES 
            (%(icao24)s, %(callsign)s, %(origin_country)s, %(longitude)s, %(latitude)s, %(altitude)s, %(velocity)s, %(timestamp)s)
    """
    cursor.executemany(query, flights)
    
# Main loop
if __name__ == "__main__":
    print("Consumer started")
    conn = psycopg2.connect(**DB_CONFIG)
    conn.autocommit = False

    batch = []

    for message in consumer:
        flight = message.value
        batch.append(flight)

        if len(batch) >= 100:
            with conn.cursor() as cursor:
                insert_flights(cursor, batch)
            conn.commit()
            print(f"Inserted batch of {len(batch)} flights - {datetime.now()}")
            batch = []