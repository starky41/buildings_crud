
from database.models import BuildingDescription
from database.database import db_session
from constants import field_labels
from sqlalchemy.orm import joinedload
from constants import LABELS
from database.data_access_layer import DataAccessLayer
from ..widgets.sortable_table_widget import SortableTableWidget
from .add_record_dialog import AddRecordDialog
from .update_record_dialog import UpdateRecordDialog
from gui.tab2.tab2 import Tab2

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QMessageBox,
    QHBoxLayout, QTableWidgetItem
) 
from database.models import WearRate

from gui.tab1.wear_rate.wear_rate import WearRateDialog


class MainWidget(QWidget):
    # Translated column names
    translation_dict = {
        "ID_building": "ИД",
        "street_name": "Улица",
        "house": "Дом",
        "building_body": "Корпус",
        "latitude": "Широта",
        "longitude": "Долгота",
        "year_construction": "Год постройки",
        "number_floors": "Кол-во этажей",
        "number_entrances": "Кол-во подъездов",
        "number_buildings": "Кол-во строений",
        "number_living_quarters": "Кол-во жилых помещений",
        "title": "Название",
        "type_construction_name": "Тип конструкции",
        "basic_project_name": "Типовой проект",
        "appointment_name": "Назначение",
        "seismic_resistance_min": "Мин сейсмостойкость",
        "seismic_resistance_max": "Макс сейсмостойкость",
        "zone_SMZ_min": "Мин зона СМЗ",
        "zone_SMZ_max": "Макс зона СМЗ",
        "priming": "Грунт",
        "load_bearing_walls_name": "Несущие стены",
        "basement_area": "Площадь подвала",
        "building_roof_name": "Крыша",
        "building_floor_name": "Перекрытия",
        "facade_name": "Фасад",
        "foundation_name": "Фундамент",
        "azimuth": "Азимут",
        "cadastral_number": "Кадастровый номер",
        "cadastral_cost": "Кадастровая стоимость",
        "year_overhaul": "Год капремонта",
        "accident_rate": "Аварийность",
        "management_company_name": "Упр компания",
        "Land_area": "Площадь земельного участка",
        "notes": "Примечания",
        "author": "Автор"
    }

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Описания зданий")
        self.initUI()

        # Initialize substituted_values dictionary
        self.substituted_values = {}

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.dal = DataAccessLayer(db_session)
        self.table_widget = SortableTableWidget()
        self.tab2 = Tab2()  # Assuming an instance of Tab2 is available
        self.table_widget.setColumnCount(len(self.translation_dict))
        translated_headers = [self.translation_dict[key] for key in self.translation_dict]
        self.table_widget.setHorizontalHeaderLabels(translated_headers)
        layout.addWidget(self.table_widget)
        self.resize(1280, 720)  

        # Add buttons for Delete, Update, and Add Record
        button_layout = QHBoxLayout()
        layout.addLayout(button_layout)

        delete_button = QPushButton("Удалить")
        delete_button.clicked.connect(self.delete_selected_record)
        button_layout.addWidget(delete_button)

        update_button = QPushButton("Изменить")
        update_button.clicked.connect(self.update_record)
        button_layout.addWidget(update_button)

        add_record_button = QPushButton("Создать")
        add_record_button.clicked.connect(self.add_record)
        button_layout.addWidget(add_record_button)

        wear_rate_button = QPushButton('Износ')
        wear_rate_button.clicked.connect(self.open_wear_rate_for_current_record)
        button_layout.addWidget(wear_rate_button)

        # Populate the table with data
        self.populate_table()

    def populate_table(self):
        # Fetch data from the database with eager loading of related attributes
        session = db_session()
        data = session.query(BuildingDescription).options(
            joinedload(BuildingDescription.street),
            joinedload(BuildingDescription.type_construction),
            joinedload(BuildingDescription.basic_project),
            joinedload(BuildingDescription.appointment),
            joinedload(BuildingDescription.load_bearing_walls),
            joinedload(BuildingDescription.building_roof),
            joinedload(BuildingDescription.building_floor),
            joinedload(BuildingDescription.facade),
            joinedload(BuildingDescription.foundation),
            joinedload(BuildingDescription.management_company)
        ).all()

        self.table_widget.setRowCount(len(data))

        # Populate the table with data
        for row_index, row_data in enumerate(data):
            for col_index, header in enumerate(self.translation_dict):
                cell_value = ""

                if hasattr(row_data, header):
                    # Check if the attribute exists directly in BuildingDescription
                    cell_value = getattr(row_data, header)
                elif hasattr(row_data, header + "_name"):
                    # Check if the attribute exists with "_name" suffix (indicating the name of the related object)
                    cell_value = getattr(row_data, header + "_name")
                else:
                    # Handle the case where the attribute does not exist directly or as a related object's name
                    # Assume it's a foreign key and retrieve the related object's name
                    related_model_name = header.replace("_name", "")
                    related_instance = getattr(row_data, related_model_name, None)
                    if related_instance:
                        # Check if the attribute exists in the related model
                        cell_value = getattr(related_instance, related_model_name + "_name", "")

                # Set the cell value in the table
                cell_value = str(cell_value) if cell_value is not None else ""  # Convert None to empty string
                self.table_widget.setItem(row_index, col_index, QTableWidgetItem(cell_value))

        session.close()
    def update_record(self):
        selected_rows = self.table_widget.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "Предупреждение", "Выберите запись для изменения.")
            return

        row_index = selected_rows[0].row()
        record_data = {}
        for col_index, header in enumerate(self.translation_dict):
            translated_header = self.translation_dict[header]
            record_data[header] = self.table_widget.item(row_index, col_index).text()

        update_dialog = UpdateRecordDialog(record_data)
        update_dialog.exec()

        self.populate_table()



    def add_record(self):
        # Open the Add Record dialog
        add_record_dialog = AddRecordDialog()
        add_record_dialog.exec()

        # Refresh the table after adding a record
        self.populate_table()

    def delete_selected_record(self):
        selected_rows = self.table_widget.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "Предупреждение", "Пожалуйста, выберите запись для удаления")
            return

        # Assuming only one row can be selected at a time
        row_index = selected_rows[0].row()
        cell_text = self.table_widget.item(row_index, 0).text()  # Assuming the first column contains the primary key
        try:
            record_id = int(cell_text)
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Неверное значение идентификатора записи.")
            return

        try:
            self.dal.delete(BuildingDescription, ID_building=record_id)
            # Remove the row from the table
            self.table_widget.removeRow(row_index)
            QMessageBox.information(self, "Успешно", "Запись успешно удалена.")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"При удалении записи возникла ошибка: {str(e)}")

    def open_wear_rate_for_current_record(self):
        selected_rows = self.table_widget.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "Предупреждение", "Пожалуйста, выберите запись для которой вы хотите открыть таблицу \"Износ\".")
            return

        row_index = selected_rows[0].row()
        record_id_item = self.table_widget.item(row_index, 0)  # Assuming the ID_building is in the first column
        building_id = int(record_id_item.text())

        session = db_session()
        wear_rates = session.query(WearRate).filter(WearRate.ID_building == building_id).all()
        session.close()

        # Prepare data for the dialog
        wear_rate_data = []
        for rate in wear_rates:
            wear_rate_data.append({
                "ИД": rate.ID_wear_rate,
                "Дата": rate.date,
                "Степень износа": rate.wear_rate_name
            })

        wear_rate_dialog = WearRateDialog(wear_rate_data, building_id)
        wear_rate_dialog.exec()




