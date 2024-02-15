from models import *
from database import init_db, db_session
from data_access_layer import DataAccessLayer
from sqlalchemy.exc import IntegrityError
def populate_database():
    # Initialize the DataAccessLayer instance
    dal = DataAccessLayer(db_session)

    # Define all the data for the 10 tables
    street_data = [
        "Абеля", "Академика Заварицкого А.Н.", "Арсеньева",
        "бульвар Пийпа", "Кавказская", "Карагинская",
        "Карбышева", "Маршала Блюхера", "Молчанова",
        "проспект Победы", "Флотская", "Чубарова", "Якорная"
    ]
    appointment_data = [
        "административное здание", "бассейн", "детский сад", "кафе",
        "котельная", "магазин", "медицинское учреждение",
        "многоквартирный дом", "образовательное учреждение",
        "общежитие", "пищекомбинат", "почта", "производственное здание",
        "средняя школа", "торговый центр", "частный", "школа-детский сад"
    ]
    title_data = [
        "Камчатский морской энергетический техникум",
        "Камчатский политехнический техникум",
        "Камчатское управление по гидрометеорологии и мониторингу окружающей среды",
        "Краевой кожно-венерологический диспансер"
    ]
    type_construction_data = ["блочный", "деревянный", "каркасно-панельное", "каркасно-панельный",
                              "крупноблочный", "металлоконструкция", "панельный"]
    load_bearing_walls_data = ["блочные", "панельные"]
    building_roof_data = ["плоская"]
    building_floor_data = ["железобетонные"]
    facade_data = ["иной", "облицованный камнем", "окрашенный", "оштукатуренный", "сайдинг",
                   "соответствует материалу стен"]
    foundation_data = ["иной", "ленточный", "сборный"]
    basic_project_data = ["1-138", "1-138с", "1-138с*", "1-306с", "1-307с", "138с", "1-464-АС",
                          "1-464АС-17к", "434-АС", "м"]

    # Iterate through each item and populate the tables
    for street, appointment in zip(street_data, appointment_data):
        new_street = Street(street_name=street)
        new_appointment = Appointment(appointment_name=appointment)
        dal.create(new_street)
        dal.create(new_appointment)

    for title in title_data:
        new_building_description = BuildingDescription(title=title)
        dal.create(new_building_description)

    # Populate the rest of the tables (assuming there are constructors for each table)
    for type_construction in type_construction_data:
        dal.create(TypeConstruction(type_construction_name=type_construction))

    for wall in load_bearing_walls_data:
        dal.create(LoadBearingWalls(load_bearing_walls_name=wall))

    for roof in building_roof_data:
        dal.create(BuildingRoof(building_roof_name=roof))

    for floor in building_floor_data:
        dal.create(BuildingFloor(building_floor_name=floor))

    for facade in facade_data:
        dal.create(Facade(facade_name=facade))

    for foundation in foundation_data:
        dal.create(Foundation(foundation_name=foundation))

    for project in basic_project_data:
        dal.create(BasicProject(basic_project_name=project))


try:
    populate_database()
except IntegrityError as e:
    print(f"ERROR: {e}")

