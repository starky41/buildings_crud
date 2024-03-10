from database.models import Street, TypeConstruction, BasicProject, Appointment, LoadBearingWalls, BuildingRoof, BuildingFloor, Facade, BuildingDescription, WearRate, Foundation, ManagementCompany
field_labels = {
            "ID_street": "Улица",
            "house": "Дом",
            "building_body": "Корпус",
            "latitude": "Широта",
            "longitude": "Долгота",
            "year_construction": "Год постройки",
            "number_floors": "Количество этажей",
            "number_entrances": "Количество подъездов",
            "number_buildings": "Количество строений",
            "number_living_quarters": "Количество жилых помещений",
            "title": "Название",
            "ID_type_construction": "Тип конструкции",
            "ID_basic_project": "Типовой проект",
            "ID_appointment": "Назначение",
            "seismic_resistance_min": "Расчетная сейсмостойкость min",
            "seismic_resistance_max": "Расчетная сейсмостойкость max",
            "zone_SMZ_min": "Зона по карте СМР min",
            "zone_SMZ_max": "Зона по карте СМР max",
            "priming": "Грунт",
            "ID_load_bearing_walls": "Несущие стены",
            "basement_area": "Площадь подвала",
            "ID_building_roof": "Крыша",
            "ID_building_floor": "Перекрытия",
            "ID_facade": "Фасад",
            "ID_foundation": "Фундамент",
            "azimuth": "Расположение по сторонам света",
            "cadastral_number": "Кадастровый номер",
            "cadastral_cost": "Кадастровая стоимость",
            "year_overhaul": "Год капремонта",
            "accident_rate": "Аварийность",
            "ID_management_company": "Управляющая компания",
            "Land_area": "Площадь земельного участка общего имущества м2",
            "notes": "Примечания",
            "author": "Источник данных"
        }

LABELS = [  # Store labels and their respective data types
            ("ID_street", "VARCHAR(150)", Street), ("house", "VARCHAR(150)", None), ("building_body", "int", None),
            ("latitude", "numeric", None), ("longitude", "numeric", None), ("year_construction", "int", None),
            ("number_floors", "int", None), ("number_entrances", "int", None), ("number_buildings", "int", None),
            ("number_living_quarters", "int", None), ("title", "VARCHAR(150)", None),
            ("ID_type_construction", "VARCHAR(150)", TypeConstruction), ("ID_basic_project", "VARCHAR(150)", BasicProject),
            ("ID_appointment", "VARCHAR(150)", Appointment), ("seismic_resistance_min", "numeric", None),
            ("seismic_resistance_max", "numeric", None), ("zone_SMZ_min", "numeric", None),
            ("zone_SMZ_max", "numeric", None), ("priming", "VARCHAR(150)", None),
            ("ID_load_bearing_walls", "VARCHAR(150)", LoadBearingWalls), ("basement_area", "numeric", None),
            ("ID_building_roof", "VARCHAR(150)", BuildingRoof), ("ID_building_floor", "VARCHAR(150)", BuildingFloor),
            ("ID_facade", "VARCHAR(150)", Facade), ("ID_foundation", "VARCHAR(150)", Foundation),
            ("azimuth", "VARCHAR(150)", None), ("cadastral_number", "int", None),
            ("cadastral_cost", "numeric", None), ("year_overhaul", "int", None),
            ("accident_rate", "VARCHAR(150)", None), ("ID_management_company", "VARCHAR(150)", ManagementCompany),
            ("Land_area", "numeric", None), ("notes", "VARCHAR(150)", None),
            ("author", "VARCHAR(150)", None)
        ]field_labels = {
            "ID_street": "Улицы",
            "house": "Дом",
            "building_body": "Корпус",
            "latitude": "Широта",
            "longitude": "Долгота",
            "year_construction": "Год постройки",
            "number_floors": "Количество этажей",
            "number_entrances": "Количество подъездов",
            "number_buildings": "Количество строений",
            "number_living_quarters": "Количество жилых помещений",
            "title": "Название",
            "ID_type_construction": "Тип конструкции",
            "ID_basic_project": "Типовой проект",
            "ID_appointment": "Назначение",
            "seismic_resistance_min": "Расчетная сейсмостойкость min",
            "seismic_resistance_max": "Расчетная сейсмостойкость max",
            "zone_SMZ_min": "Зона по карте СМР min",
            "zone_SMZ_max": "Зона по карте СМР max",
            "priming": "Грунт",
            "ID_load_bearing_walls": "Несущие стены",
            "basement_area": "Площадь подвала",
            "ID_building_roof": "Крыша",
            "ID_building_floor": "Перекрытия",
            "ID_facade": "Фасад",
            "ID_foundation": "Фундамент",
            "azimuth": "Расположение по сторонам света",
            "cadastral_number": "Кадастровый номер",
            "cadastral_cost": "Кадастровая стоимость",
            "year_overhaul": "Год капремонта",
            "accident_rate": "Аварийность",
            "ID_management_company": "Управляющая компания",
            "Land_area": "Площадь земельного участка общего имущества м2",
            "notes": "Примечания",
            "author": "Источник данных"
        }