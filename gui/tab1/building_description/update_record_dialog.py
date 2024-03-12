from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QCompleter, QMessageBox, QGridLayout
)
from PyQt6.QtGui import QIntValidator, QDoubleValidator
from PyQt6.QtCore import QStringListModel
from database.models import BuildingDescription
from database.database import db_session
from constants import field_labels
from sqlalchemy.orm import joinedload
from constants import LABELS
from database.data_access_layer import DataAccessLayer
from database.models import *
LABEL_TRANSLATIONS = {
    "ID_building": "ИД_здания",
    "street_name": "Название_улицы",
    "house": "Дом",
    "building_body": "Корпус",
    "latitude": "Широта",
    "longitude": "Долгота",
    "year_construction": "Год_строительства",
    "number_floors": "Кол-во_этажей",
    "number_entrances": "Кол-во_подъездов",
    "number_buildings": "Кол-во_зданий",
    "number_living_quarters": "Кол-во_жилых_помещений",
    "title": "Заголовок",
    "type_construction_name": "Тип_конструкции",
    "basic_project_name": "Основной_проект",
    "appointment_name": "Назначение",
    "seismic_resistance_min": "Мин_сейсмостойкость",
    "seismic_resistance_max": "Макс_сейсмостойкость",
    "zone_SMZ_min": "Мин_зона_СМЗ",
    "zone_SMZ_max": "Макс_зона_СМЗ",
    "priming": "Грунтовка",
    "load_bearing_walls_name": "Название_несущих_стен",
    "basement_area": "Площадь_подвала",
    "building_roof_name": "Название_крыши",
    "building_floor_name": "Название_пола_здания",
    "facade_name": "Фасад",
    "foundation_name": "Фундамент",
    "azimuth": "Азимут",
    "cadastral_number": "Кадастровый_номер",
    "cadastral_cost": "Кадастровая_стоимость",
    "year_overhaul": "Год_капремонта",
    "accident_rate": "Коэффициент_аварийности",
    "management_company_name": "Название_управляющей_компании",
    "Land_area": "Площадь_земли",
    "notes": "Примечания",
    "author": "Автор"
}

class UpdateRecordDialog(QDialog):
    def __init__(self, record_data):
        super().__init__()
        self.setWindowTitle("Изменение записи")
        self.record_data = record_data
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.line_edits = {}  # Initialize a dictionary to store line edits
        grid_layout = QGridLayout()
        layout.addLayout(grid_layout)

        self.labels = LABELS

        # Include 'street_name' in the required fields
        required_fields = ["street_name"]

        num_columns = 2  # Number of columns in the grid layout
        row_index = 0  # Track the row index
        col_index = 0  # Track the column index
        for idx, (label_text, value) in enumerate(self.record_data.items()):
            if label_text == "ID_building":
                continue  # Skip adding ID_building to the layout

            label_text_russian = LABEL_TRANSLATIONS.get(label_text, label_text)
            if label_text == "ID_street":
                label_text_russian = "Название улицы"  # Replace ID_street with street_name
            label = QLabel(label_text_russian.replace('_', ' '))  # Replacing underscores with spaces for better readability
            line_edit = QLineEdit()

            # Add validator based on data type
            validator = None
            if label_text in ("building_body", "cadastral_number", "year_construction", "number_floors",
                            "number_entrances", "number_buildings", "number_living_quarters", "cadastral_cost",
                            "year_overhaul", "Land_area"):
                validator = QIntValidator()
            elif label_text in ("latitude", "longitude", "seismic_resistance_min", "seismic_resistance_max",
                                "zone_SMZ_min", "zone_SMZ_max", "basement_area"):
                validator = QDoubleValidator()

            if validator:
                line_edit.setValidator(validator)

            # Prefill the line edit with existing data
            if value is not None:
                line_edit.setText(str(value))

            # Adjusting layout for two columns
            if col_index >= num_columns:
                row_index += 1
                col_index = 0

            grid_layout.addWidget(label, row_index, col_index * 2)  # Add the label to the grid
            grid_layout.addWidget(line_edit, row_index, col_index * 2 + 1)  # Add the line edit to the grid
            self.line_edits[label_text] = line_edit  # Store line edit in the dictionary

            # Set up QCompleter if needed
            if label_text in ("street_name", "type_construction_name", "basic_project_name", "appointment_name",
                                "load_bearing_walls_name", "building_roof_name", "building_floor_name", "facade_name",
                                "foundation_name", "management_company_name"):
                completer = QCompleter()
                line_edit.setCompleter(completer)
                session = db_session()  # Assuming db_session is your SQLAlchemy session

                query_classes = {
                    "street_name": Street,
                    "type_construction_name": TypeConstruction,
                    "basic_project_name": BasicProject,
                    "appointment_name": Appointment,
                    "load_bearing_walls_name": LoadBearingWalls,
                    "building_roof_name": BuildingRoof,
                    "building_floor_name": BuildingFloor,
                    "facade_name": Facade,
                    "foundation_name": Foundation,
                    "management_company_name": ManagementCompany
                }

                if label_text in query_classes:
                    data_query = session.query(query_classes[label_text]).distinct().all()

                session.close()

                data = [getattr(item, label_text) for item in data_query]
                completer.setModel(QStringListModel(data))

            col_index += 1

        save_button = QPushButton("Save")
        save_button.clicked.connect(self.update_record)
        layout.addWidget(save_button)
    def update_record(self):
        # Get updated data from the form fields
        updated_data = {}
        required_fields = ["street_name", "house"]  # Specify the required fields

        # Check if the required fields are empty
        for field in required_fields:
            if not self.line_edits.get(field):
                print(f"DEBUG: Field '{field}' not found in line edits.")
                QMessageBox.warning(self, "Предупреждение", f"Пожалуйста введите значение в поле {field}.")
                return

        for label_text, line_edit in self.line_edits.items():
            value = line_edit.text()
            if value:  # Check if the value is not empty
                updated_data[label_text] = value

        # Convert name values to ID values for applicable fields
        for label_text, data_type, related_model in self.labels:
            if label_text.startswith("ID_") and related_model:
                session = db_session()
                name_value = updated_data.get(label_text.replace("ID_", "") + "_name", "")
                if name_value:
                    # Query the related table to find the ID corresponding to the name value
                    related_instance = session.query(related_model).filter_by(**{related_model.__tablename__ + "_name": name_value}).first()
                    session.close()
                    if related_instance:
                        updated_data[label_text] = getattr(related_instance, "ID_" + related_model.__tablename__)
                    else:
                        QMessageBox.warning(self, "Предупреждение", f"Не найдена запись для значения {name_value} в таблице {related_model.__tablename__}.")
                        return

        print(f"\n\nUpdated data: {updated_data}\n\n")  # Debug print to check the updated data

        # Update the record in the database
        session = db_session()
        record_id = self.record_data.get("ID_building")
        record = session.query(BuildingDescription).filter_by(ID_building=record_id).first()

        if record:
            print(f"\n\nExisting record: {record.__dict__}\n\n")  # Debug print to check the existing record before update
            try:
                for key, value in updated_data.items():
                    if hasattr(record, key):
                        setattr(record, key, value)
                    else:
                        # If the key doesn't exist in the record, skip it
                        print(f"Предупреждение: ключ '{key}' не найден для записи.")
            except Exception as e:
                session.rollback()
                QMessageBox.warning(self, "Ошибка", f"Не удалось обновить запись: {str(e)}")
                return

            try:
                session.commit()
                QMessageBox.information(self, "Успешно", "Запись успешно обновлена.")
                self.close()
            except Exception as e:
                session.rollback()
                QMessageBox.warning(self, "Ошибка", f"При изменении записи возникла ошибка: {str(e)}")
        else:
            QMessageBox.warning(self, "Ошибка", "Запись не найдена.")

        session.close()

# Example usage:
# dialog = UpdateRecordDialog(record_data=your_record_data)
# dialog.exec()
