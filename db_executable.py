# A helper function to generate foreign key statements.
def create_foreign_key(fk_field, reference_table):
    return f", FOREIGN KEY ({fk_field}) REFERENCES {reference_table}({fk_field})"


sql_create_tables = """
    CREATE TABLE IF NOT EXISTS street(
        ID_street INT PRIMARY KEY,
        street_name VARCHAR(150)
    );
    
    CREATE TABLE IF NOT EXISTS type_construction(
        ID_type_construction INT PRIMARY KEY,
        type_construction_name VARCHAR(150)
    );
    
    CREATE TABLE IF NOT EXISTS basic_project(
        ID_basic_project INT PRIMARY KEY,
        basic_project_name VARCHAR(150)
    );
    
    CREATE TABLE IF NOT EXISTS appointment(
        ID_appointment INT PRIMARY KEY,
        appointment_name VARCHAR(150)
    );
    
    CREATE TABLE IF NOT EXISTS load_bearing_walls(
        ID_load_bearing_walls INT PRIMARY KEY,
        load_bearing_walls_name VARCHAR(150)
    );
    
    CREATE TABLE IF NOT EXISTS building_roof(
        ID_building_roof INT PRIMARY KEY,
        building_floor_name VARCHAR(150)
    );
    
    CREATE TABLE IF NOT EXISTS building_floor(
        ID_building_floor INT PRIMARY KEY,
        building_floor_name VARCHAR(150)
    );
    
    CREATE TABLE IF NOT EXISTS facade(
        ID_facade INT PRIMARY KEY,
        facade_name VARCHAR(150)
    );
    
    CREATE TABLE IF NOT EXISTS foundation(
        ID_foundation INT PRIMARY KEY,
        foundation_name VARCHAR(150)    
    );
    
    CREATE TABLE IF NOT EXISTS management_company(
        ID_management_company INT PRIMARY KEY,
        management_company_name VARCHAR(150)
    );
    
"""

sql_create_building_description = f'''
    CREATE TABLE IF NOT EXISTS building_description(
        ID_building INT PRIMARY KEY,
        ID_street INT,
        house INT,
        building_body INT,
        latitude NUMERIC,
        longitude NUMERIC,
        year_construction INT,
        number_floors INT,
        number_entrances INT,
        number_buildings INT,
        number_living_quarters INT,
        title VARCHAR(150),
        ID_type_construction INT,
        ID_basic_project INT,
        ID_appointment INT,
        seismic_resistance_max NUMERIC,
        seismic_resistance_min NUMERIC,
        seismic_resistance_soft NUMERIC,
        zone_SMZ_min NUMERIC,
        zone_SMZ_max NUMERIC,
        zone_SMZ_increment NUMERIC,
        priming VARCHAR(150),
        ID_load_bearing_walls INT,
        basement_area NUMERIC,
        ID_building_roof INT,
        ID_building_floor INT,
        ID_facade INT,
        ID_foundation INT,
        azimuth VARCHAR(150),
        cadastral_number INT,
        cadastral_cost NUMERIC,
        year_overhaul INT,
        accident_rate VARCHAR(150),
        ID_management_company INT,
        Land_area NUMERIC,
        notes VARCHAR(150),
        author VARCHAR(150)
        
        {create_foreign_key('ID_street', 'street')}
        {create_foreign_key('ID_type_construction', 'type_construction')}
        {create_foreign_key('ID_basic_project', 'basic_project')}
        {create_foreign_key('ID_appointment', 'appointment')}
        {create_foreign_key('ID_load_bearing_walls', 'load_bearing_walls')}
        {create_foreign_key('ID_building_roof', 'building_roof')}
        {create_foreign_key('ID_building_floor', 'building_floor')}
        {create_foreign_key('ID_facade', 'facade')}
        {create_foreign_key('ID_foundation', 'foundation')}  
        {create_foreign_key('ID_management_company', 'management_company')}     
    
    );
'''

sql_query = sql_create_tables + sql_create_building_description
