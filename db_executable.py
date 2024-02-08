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
        ID_basic_project INT PRIMARY KEY,
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