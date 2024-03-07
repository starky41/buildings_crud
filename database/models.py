from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, Date
from sqlalchemy.orm import relationship
from database.database import Base

class Street(Base):
    __tablename__ = 'street'
    ID_street = Column(Integer, primary_key=True, autoincrement=True) 
    street_name = Column(String(150), unique=True, nullable=False)

class TypeConstruction(Base):
    __tablename__ = 'type_construction'
    ID_type_construction = Column(Integer, primary_key=True, autoincrement=True)
    type_construction_name = Column(String(150), unique=True, nullable=False)
    
class BasicProject(Base):
    __tablename__ = 'basic_project'
    ID_basic_project = Column(Integer, primary_key=True, autoincrement=True)
    basic_project_name = Column(String(150), unique=True, nullable=False)

class Appointment(Base):
    __tablename__ = 'appointment'
    ID_appointment = Column(Integer, primary_key=True, autoincrement=True)
    appointment_name = Column(String(150), unique=True, nullable=False)

class LoadBearingWalls(Base):
    __tablename__ = 'load_bearing_walls'
    ID_load_bearing_walls = Column(Integer, primary_key=True, autoincrement=True)
    load_bearing_walls_name = Column(String(150), unique=True, nullable=False)

class BuildingRoof(Base):
    __tablename__ = 'building_roof'
    ID_building_roof = Column(Integer, primary_key=True, autoincrement=True)
    building_roof_name = Column(String(150), unique=True, nullable=False)

class BuildingFloor(Base):
    __tablename__ = 'building_floor'
    ID_building_floor = Column(Integer, primary_key=True, autoincrement=True)
    building_floor_name = Column(String(150), unique=True, nullable=False)

class Facade(Base):
    __tablename__ = 'facade'
    ID_facade = Column(Integer, primary_key=True, autoincrement=True)
    facade_name = Column(String(150), unique=True, nullable=False)

class Foundation(Base):
    __tablename__ = 'foundation'
    ID_foundation = Column(Integer, primary_key=True, autoincrement=True)
    foundation_name = Column(String(150), unique=True, nullable=False)

class ManagementCompany(Base):
    __tablename__ = 'management_company'
    ID_management_company = Column(Integer, primary_key=True, autoincrement=True)
    management_company_name = Column(String(150), unique=True, nullable=False)

class BuildingDescription(Base):
    __tablename__ = 'building_description'

    ID_building = Column(Integer, primary_key=True, autoincrement=True)
    ID_street = Column(Integer, ForeignKey('street.ID_street'))
    house = Column(String(150))
    building_body = Column(Integer)
    latitude = Column(Numeric)
    longitude = Column(Numeric)
    year_construction = Column(Integer)
    number_floors = Column(Integer)
    number_entrances = Column(Integer)
    number_buildings = Column(Integer)
    number_living_quarters = Column(Integer)
    title = Column(String(150))
    ID_type_construction = Column(Integer, ForeignKey('type_construction.ID_type_construction'))
    ID_basic_project = Column(Integer, ForeignKey('basic_project.ID_basic_project'))
    ID_appointment = Column(Integer, ForeignKey('appointment.ID_appointment'))
    seismic_resistance_max = Column(Numeric, unique=True)
    seismic_resistance_min = Column(Numeric, unique=True)
    seismic_resistance_soft = Column(Numeric, unique=True)
    zone_SMZ_min = Column(Numeric)
    zone_SMZ_max = Column(Numeric)
    zone_SMZ_increment = Column(Numeric)
    priming = Column(String(150))
    ID_load_bearing_walls = Column(Integer, ForeignKey('load_bearing_walls.ID_load_bearing_walls'))
    basement_area = Column(Numeric)
    ID_building_roof = Column(Integer, ForeignKey('building_roof.ID_building_roof'))
    ID_building_floor = Column(Integer, ForeignKey('building_floor.ID_building_floor'))
    ID_facade = Column(Integer, ForeignKey('facade.ID_facade'))
    ID_foundation = Column(Integer, ForeignKey('foundation.ID_foundation'))
    azimuth = Column(String(150))
    cadastral_number = Column(Integer)
    cadastral_cost = Column(Numeric)
    year_overhaul = Column(Integer)
    accident_rate = Column(String(150))
    ID_management_company = Column(Integer, ForeignKey('management_company.ID_management_company'))
    Land_area = Column(Numeric)
    notes = Column(String(150))
    author = Column(String(150))

    # Define relationships to access related objects easily through ORM (optional)
    street = relationship('Street')
    type_construction = relationship('TypeConstruction')
    basic_project = relationship('BasicProject')
    appointment = relationship('Appointment')
    load_bearing_walls = relationship('LoadBearingWalls')
    building_roof = relationship('BuildingRoof')
    building_floor = relationship('BuildingFloor')
    facade = relationship('Facade')
    foundation = relationship('Foundation')
    management_company = relationship('ManagementCompany')

class WearRate(Base):
    __tablename__ = 'wear_rate'
    ID_wear_rate = Column(Integer, primary_key=True)
    date = Column(Date)
    wear_rate_name = Column(String(150))
    ID_building = Column(Integer, ForeignKey('building_description.ID_building'))

    # Relationship to access building_description records from a wear_rate instance
    building_description = relationship('BuildingDescription')

