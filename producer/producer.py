import json
import time
import requests
from kafka import KafkaProducer

KAFKA_BROKER = "localhost:9092"
TOPIC = "flights-raw"
API_URL = "https://opensky-network.org/api/states/all"
INTERVAL_SECONDS = 30

# Initialize the producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

# Fetch flights
def fetch_flights():
    try:
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("states", [])
    except Exception as e:
        print(f"Error fetching data: {e}")
        return []
    
# Publish flights
def publish_flights(flights):
    for flight in flights:
        message = {
            "icao24": flight[0],
            "callsign": flight[1],
            "origin_country": flight[2],
            "longitude": flight[5],
            "latitude": flight[6],
            "altitude": flight[7],
            "velocity": flight[9],
            "timestamp": int(time.time())
        }
        producer.send(TOPIC, value=message)
    producer.flush()
    print(f"Published {len(flights)} flights")
    
# Main loop
if __name__ == "__main__":
    print("Producer started")
    while True:
        flights = fetch_flights()
        if flights:
            publish_flights(flights)
        time.sleep(INTERVAL_SECONDS)