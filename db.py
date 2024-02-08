import psycopg2
from db_executable import sql_create_tables

# This connection string should match the one in your Python code
conn_string = "host='localhost' dbname='my_db' user='starky' password='1234'"

# Connect to your PostgreSQL database
conn = psycopg2.connect(conn_string)

# Create a cursor object
cursor = conn.cursor()

cursor.execute(sql_create_tables)

conn.commit()

cursor.close()
conn.close()
