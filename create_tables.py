# Define table structures
table_definitions = {
    "street": {
        "ID_street": "INT PRIMARY KEY",
        "street_name": "VARCHAR(150)"
    },
    "type_construction": {
        "ID_type_construction": "INT PRIMARY KEY",
        "type_construction_name": "VARCHAR(150)"
    },
    "basic_project": {
        "ID_basic_project": "INT PRIMARY KEY",
        "basic_project_name": "VARCHAR(150)"
    },
    "appointment": {
        "ID_appointment": "INT PRIMARY KEY",
        "appointment_name": "VARCHAR(150)"
    },
    "load_bearing_walls": {
        "ID_load_bearing_walls": "INT PRIMARY KEY",
        "load_bearing_walls_name": "VARCHAR(150)"
    },
    "building_roof": {
        "ID_building_roof": "INT PRIMARY KEY",
        "building_roof_name": "VARCHAR(150)"
    },
    "building_floor": {
        "ID_building_floor": "INT PRIMARY KEY",
        "building_floor_name": "VARCHAR(150)"
    },
    "facade": {
        "ID_facade": "INT PRIMARY KEY",
        "facade_name": "VARCHAR(150)"
    },
    "foundation": {
        "ID_foundation": "INT PRIMARY KEY",
        "foundation_name": "VARCHAR(150)"
    },
    "management_company": {
        "ID_management_company": "INT PRIMARY KEY",
        "management_company_name": "VARCHAR(150)"
    }
}


# Function to generate CREATE TABLE SQL statement for a given table
def create_table_sql(table_name, column_definitions, foreign_key_constraints=""):
    columns_sql = ",\n    ".join(f"{column_name} {data_type}" for column_name, data_type in column_definitions.items())
    if foreign_key_constraints:
        foreign_key_sql = ",\n    " + foreign_key_constraints
    else:
        foreign_key_sql = ""

    create_table_statement = f"""CREATE TABLE IF NOT EXISTS {table_name}(
    {columns_sql}{foreign_key_sql}
);"""

    return create_table_statement


# Generate all CREATE TABLE SQL statements
sql_create_tables = "".join(create_table_sql(name, fields) for name, fields in table_definitions.items())

foreign_keys = [
    ('ID_street', 'street'),
    ('ID_type_construction', 'type_construction'),
    ('ID_basic_project', 'basic_project'),
    ('ID_appointment', 'appointment'),
    ('ID_load_bearing_walls', 'load_bearing_walls'),
    ('ID_building_roof', 'building_roof'),
    ('ID_building_floor', 'building_floor'),
    ('ID_facade', 'facade'),
    ('ID_foundation', 'foundation'),
    ('ID_management_company', 'management_company'),
]


# Function to create foreign key SQL string
def create_foreign_key(column, referenced_table):
    return f"FOREIGN KEY ({column}) REFERENCES {referenced_table}({column})"


# Construct the foreign key constraints SQL by joining the definitions with commas
foreign_key_sql = ",\n    ".join(create_foreign_key(column, table) for column, table in foreign_keys)

# Here's how you might include this within the create_table_sql:
sql_create_building_description = create_table_sql("building_description", {
    "ID_building": "INT PRIMARY KEY",
    "ID_street": "INT",
    "house": "INT",
    "building_body": "INT",
    "latitude": "NUMERIC",
    "longitude": "NUMERIC",
    "year_construction": "INT",
    "number_floors": "INT",
    "number_entrances": "INT",
    "number_buildings": "INT",
    "number_living_quarters": "INT",
    "title": "VARCHAR(150)",
    "ID_type_construction": "INT",
    "ID_basic_project": "INT",
    "ID_appointment": "INT",
    "seismic_resistance_max": "NUMERIC",
    "seismic_resistance_min": "NUMERIC",
    "seismic_resistance_soft": "NUMERIC",
    "zone_SMZ_min": "NUMERIC",
    "zone_SMZ_max": "NUMERIC",
    "zone_SMZ_increment": "NUMERIC",
    "priming": "VARCHAR(150)",
    "ID_load_bearing_walls": "INT",
    "basement_area": "NUMERIC",
    "ID_building_roof": "INT",
    "ID_building_floor": "INT",
    "ID_facade": "INT",
    "ID_foundation": "INT",
    "azimuth": "VARCHAR(150)",
    "cadastral_number": "INT",
    "cadastral_cost": "NUMERIC",
    "year_overhaul": "INT",
    "accident_rate": "VARCHAR(150)",
    "ID_management_company": "INT",
    "Land_area": "NUMERIC",
    "notes": "VARCHAR(150)",
    "author": "VARCHAR(150)"
}, foreign_key_constraints=foreign_key_sql)


sql_query = sql_create_tables + sql_create_building_description


