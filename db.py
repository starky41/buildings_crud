import psycopg2
from create_tables import sql_query


# This connection string should match the one in your Python code
conn_string = "host='localhost' dbname='my_db' user='starky' password='1234'"

# Connect to your PostgreSQL database
conn = psycopg2.connect(conn_string)

# Create a cursor object
cursor = conn.cursor()


cursor.execute(
    '''DROP TABLE IF EXISTS street, type_construction, basic_project, appointment, load_bearing_walls, building_roof, 
    building_floor, facade, foundation, management_company, building_description, wear_rate CASCADE;
    '''
)


cursor.execute(sql_query)

conn.commit()

cursor.close()
conn.close()
