FROM python:3.11-slim

RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

RUN pip install dbt-postgres==1.10.0

WORKDIR /usr/app/dbt

ENTRYPOINT ["tail", "-f", "/dev/null"]