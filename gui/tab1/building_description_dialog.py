from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QCompleter, QMessageBox,
    QHBoxLayout, QGridLayout, QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt6.QtGui import QIntValidator, QDoubleValidator
from PyQt6.QtCore import QStringListModel, Qt
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from sqlalchemy.orm import sessionmaker
from database.models import Street, TypeConstruction, BasicProject, Appointment, LoadBearingWalls, \
    BuildingRoof, BuildingFloor, Facade, Foundation, ManagementCompany, BuildingDescription
from database.database import db_session
from constants import field_labels
from sqlalchemy.orm import joinedload
from constants import LABELS
from database.data_access_layer import DataAccessLayer
from ..widgets.sortable_table_widget import SortableTableWidget
from .add_record_dialog import AddRecordDialog
from .update_record_dialog import UpdateRecordDialog



class MainDialog(QDialog):
    table_headers = ["ID_building", "street_name", "house", "building_body", "latitude", "longitude", "year_construction",
                    "number_floors", "number_entrances", "number_buildings", "number_living_quarters",
                    "title", "type_construction_name", "basic_project_name", "appointment_name",
                    "seismic_resistance_min", "seismic_resistance_max", "zone_SMZ_min", "zone_SMZ_max",
                    "priming", "load_bearing_walls_name", "basement_area", "building_roof_name",
                    "building_floor_name", "facade_name", "foundation_name", "azimuth", "cadastral_number",
                    "cadastral_cost", "year_overhaul", "accident_rate", "management_company_name",
                    "Land_area", "notes", "author"]

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")
        self.initUI()

        # Initialize substituted_values dictionary
        self.substituted_values = {}

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.dal = DataAccessLayer(db_session)
        self.table_widget = SortableTableWidget()
        self.table_widget.setColumnCount(len(self.table_headers))
        self.table_widget.setHorizontalHeaderLabels(self.table_headers)
        layout.addWidget(self.table_widget)
        self.resize(1280, 720)  
        

        # Add buttons for Delete, Update, and Add Record
        button_layout = QHBoxLayout()
        layout.addLayout(button_layout)

        delete_button = QPushButton("Delete Selected Record")
        delete_button.clicked.connect(self.delete_selected_record)
        button_layout.addWidget(delete_button)

        update_button = QPushButton("Update Selected Record")
        update_button.clicked.connect(self.update_record)
        button_layout.addWidget(update_button)

        add_record_button = QPushButton("Add Record")
        add_record_button.clicked.connect(self.add_record)
        button_layout.addWidget(add_record_button)

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
            for col_index, header in enumerate(self.table_headers):
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
            QMessageBox.warning(self, "Warning", "Please select a record to update.")
            return

        row_index = selected_rows[0].row()
        record_data = {}
        for col_index, header in enumerate(self.table_headers):
 
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
            QMessageBox.warning(self, "Warning", "Please select a record to delete.")
            return

        # Assuming only one row can be selected at a time
        row_index = selected_rows[0].row()
        cell_text = self.table_widget.item(row_index, 0).text()  # Assuming the first column contains the primary key
        try:
            record_id = int(cell_text)
        except ValueError:
            QMessageBox.warning(self, "Error", "Invalid record ID.")
            return

        try:
            self.dal.delete(BuildingDescription, ID_building=record_id)
            # Remove the row from the table
            self.table_widget.removeRow(row_index)
            QMessageBox.information(self, "Success", "Record deleted successfully.")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to delete record: {str(e)}")
