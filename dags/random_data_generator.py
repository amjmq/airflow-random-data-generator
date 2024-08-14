from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from psycopg2 import pool
import random

# Database connection details
DB_HOST = 'postgres'
DB_NAME = 'postgres'
DB_USER = 'airflow'
DB_PASSWORD = 'airflow'

# Initialize the connection pool
conn_pool = pool.SimpleConnectionPool(
    1,  # Minimum number of connections
    10,  # Maximum number of connections
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST
)

def create_table_if_not_exists():
    conn = conn_pool.getconn()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS random_data (
                id SERIAL PRIMARY KEY,
                value INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        cursor.close()
    finally:
        conn_pool.putconn(conn)

def insert_random_data():
    conn = conn_pool.getconn()
    try:
        cursor = conn.cursor()
        random_value = random.randint(0, 100)
        cursor.execute("INSERT INTO random_data (value) VALUES (%s)", (random_value,))
        conn.commit()
        cursor.close()
    finally:
        conn_pool.putconn(conn)

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'random_data_generator',
    default_args=default_args,
    description='A simple DAG that inserts random data into PostgreSQL every 5 seconds',
    schedule_interval=timedelta(seconds=5),
    catchup=False,
)

create_table_task = PythonOperator(
    task_id='create_table_if_not_exists',
    python_callable=create_table_if_not_exists,
    dag=dag,
)

insert_data_task = PythonOperator(
    task_id='insert_random_data',
    python_callable=insert_random_data,
    dag=dag,
)

create_table_task >> insert_data_task
