# Flight Pulse

End-to-end data engineering pipeline that ingests real-time flight data
from the OpenSky Network API, streams it through Apache Kafka, stores and
transforms it with PostgreSQL and dbt, and orchestrates everything with
Apache Airflow.

## Architecture

OpenSky Network API
↓
Python Producer (every 30s)
↓
Apache Kafka — topic: flights-raw
↓
Python Consumer (batch insert)
↓
PostgreSQL — table: flights_raw
↓
dbt (staging → intermediate → marts)
↓
Apache Airflow (hourly orchestration)

## Tech Stack

| Tool | Purpose |
| --- | --- |
| Python | Producer and consumer scripts |
| Apache Kafka | Real-time message streaming |
| PostgreSQL | Data storage (raw + marts) |
| dbt | Data transformation and testing |
| Apache Airflow | Pipeline orchestration |
| Docker | Service containerization |
| Power BI | Dashboard and visualization |

## Pipeline Overview

The Airflow DAG (`flight_pipeline`) runs every hour and executes three
automated tasks:

1. **dbt_staging** — Cleans raw flight data: trims callsigns, converts
Unix timestamps to readable format, and filters null or empty records.

2. **dbt_intermediate** — Enriches the data with derived fields: hour of
day, altitude band (low / cruise / high), and speed band (slow / medium /
fast).

3. **dbt_marts** — Builds four aggregated tables ready for analysis:
flights by country, top airlines, altitude stats, and traffic by hour.

## Data Models

### Staging Layer (views)

- `stg_flights` — Cleaned flight records with formatted timestamps and
filtered nulls

### Intermediate Layer (views)

- `int_flights_cleaned` — Enriched records with altitude bands, speed
bands, and hour of day

### Marts Layer (tables)

- `mart_flights_by_country` — Total flights, avg altitude, and avg
velocity per country
- `mart_top_airlines` — Top 15 most active callsigns by total flights
- `mart_altitude_stats` — Altitude distribution (low/cruise/high) by
country
- `mart_flights_by_hour` — Flight volume and avg metrics per hour of day

## Project Structure

flight-pulse/
├── producer/          # Kafka producer — fetches from OpenSky API
├── consumer/          # Kafka consumer — inserts into PostgreSQL
├── dbt/               # dbt project (transformations + tests)
│   └── flight_pulse/
│       └── models/
│           ├── staging/
│           ├── intermediate/
│           └── marts/
├── airflow/           # Airflow DAGs and configuration
│   └── dags/
├── data/              # Exported CSV marts for Power BI
├── docs/              # Dashboard screenshots
└── docker-compose.yml

## Setup

### Prerequisites

- Python 3.11+
- Docker Desktop

### Installation

1. Clone the repository
git clone https://github.com/VladimirGarcia17/flight-pulse.git
cd flight-pulse

2. Create the environment files
cp .env.example .env
Edit .env with your credentials

3. Start all services
docker compose up -d

4. Create the Kafka topic
docker exec kafka kafka-topics --create --topic flights-raw 
--bootstrap-server localhost:9092 --partitions 1 --replication-factor 1

5. Create the flights_raw table in PostgreSQL
docker exec -it postgres psql -U flightuser -d flightdb

6. Start the producer
python producer/producer.py

7. Run dbt transformations
docker exec dbt dbt run

8. Access Airflow UI at `http://localhost:8081` and trigger the
`flight_pipeline` DAG.

## Data Source

[OpenSky Network](https://opensky-network.org/) — a community-based
receiver network that provides free real-time air traffic data.

## Author

Vladimir Garcia — [github.com/VladimirGarcia17](https://github.com/VladimirGarcia17)