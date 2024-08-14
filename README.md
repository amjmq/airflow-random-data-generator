# Random Data Generator with Apache Airflow and PostgreSQL

This project demonstrates a simple Apache Airflow DAG that generates random data and inserts it into a PostgreSQL database at regular intervals.

## Project Structure

- `dags/random_data_generator.py`: Airflow DAG definition
- `docker-compose.yml`: Docker Compose configuration file
- `Dockerfile`: Custom Airflow image definition
- `requirements.txt`: Python dependencies

## Prerequisites

- Docker
- Docker Compose

## Setup and Running

1. Clone this repository:
   ```
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Build the custom Airflow image:
   ```
   docker-compose build
   ```

3. Start the Airflow services:
   ```
   docker-compose up -d
   ```

4. Access the Airflow web interface:
   Open your browser and navigate to `http://localhost:8080`. Use the following credentials:
   - Username: airflow
   - Password: airflow

5. Enable the `random_data_generator` DAG in the Airflow web interface.

## DAG Description

The `random_data_generator` DAG performs the following tasks:

1. Creates a `random_data` table in the PostgreSQL database if it doesn't exist.
2. Inserts a random integer value (0-100) into the `random_data` table every 5 seconds.

## Database Connection

The DAG connects to a PostgreSQL database with the following details:
- Host: postgres
- Database: postgres
- User: airflow
- Password: airflow

## Customization

- To modify the DAG schedule, update the `schedule_interval` parameter in the DAG definition.
- To change the range of random values, modify the `random.randint()` function call in the `insert_random_data()` function.

## Stopping the Project

To stop and remove all containers, networks, and volumes created by Docker Compose:

```
docker-compose down -v
```

## Notes

- The PostgreSQL data is persisted in a Docker volume named `postgres-db-volume`.
- The Airflow webserver is accessible on port 8080.
- The PostgreSQL port 5432 is mapped to host port 8888 for external access if needed.

