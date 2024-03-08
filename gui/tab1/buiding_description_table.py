
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
    QHBoxLayout, QTableWidgetItem, QDialog, QLabel, QLineEdit
) 
from database.models import WearRate
from PyQt6.QtCore import Qt, pyqtSignal

class MainWidget(QWidget):
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
        self.tab2 = Tab2()  # Assuming an instance of Tab2 is available
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

        
        wear_rate_button = QPushButton('Open Wear Rate')
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

    def open_wear_rate_for_current_record(self):
        selected_rows = self.table_widget.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "Warning", "Please select a record to open Wear Rate table for.")
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
                "ID": rate.ID_wear_rate,
                "Date": rate.date,
                "Wear Rate": rate.wear_rate_name
            })

        wear_rate_dialog = WearRateDialog(wear_rate_data, building_id)
        wear_rate_dialog.exec()


from PyQt6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLabel, QTableWidgetItem, QMessageBox
from PyQt6.QtCore import Qt, pyqtSignal
from database.database import db_session
from database.models import WearRate
from datetime import date


class NewWearRateDialog(QDialog):
    record_added = pyqtSignal()

    def __init__(self, building_id):
        super().__init__()
        self.setWindowTitle("Add New Wear Rate Record")
        self.building_id = building_id
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Input fields for date and wear rate name
        self.date_input = QLineEdit()
        self.date_input.setPlaceholderText("Date (YYYY-MM-DD)")
        layout.addWidget(self.date_input)

        self.wear_rate_name_input = QLineEdit()
        self.wear_rate_name_input.setPlaceholderText("Wear Rate Name")
        layout.addWidget(self.wear_rate_name_input)

        # Add button to confirm adding the new record
        add_button = QPushButton("Add")
        add_button.clicked.connect(self.add_new_record)
        layout.addWidget(add_button)

    def add_new_record(self):
        # Retrieve input data
        date_str = self.date_input.text()
        wear_rate_name = self.wear_rate_name_input.text()

        # Validate input data
        if not date_str or not wear_rate_name:
            QMessageBox.warning(self, "Warning", "Please fill in all fields.")
            return

        try:
            # Convert date string to date object
            record_date = date.fromisoformat(date_str)
        except ValueError:
            QMessageBox.warning(self, "Error", "Invalid date format. Please use YYYY-MM-DD.")
            return

        # Create a new wear rate record
        new_wear_rate = WearRate(date=record_date, wear_rate_name=wear_rate_name, ID_building=self.building_id)

        # Add the new record to the database
        session = db_session()
        session.add(new_wear_rate)
        session.commit()
        session.close()

        # Emit signal to indicate that a new record has been added
        self.record_added.emit()

        # Close the dialog
        self.accept()


class WearRateDialog(QDialog):
    def __init__(self, wear_rate_data, building_id):
        super().__init__()
        self.setWindowTitle("Wear Rate")
        self.building_id = building_id
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.table_widget = SortableTableWidget()
        layout.addWidget(self.table_widget)

        # Check if wear rate data is available
        if wear_rate_data:
            self.populate_table(wear_rate_data)
        else:
            layout.addWidget(QLabel("No wear rate data available."))

        # Add button to add a new record
        add_button = QPushButton("Add New Record")
        add_button.clicked.connect(self.add_new_record_dialog)
        layout.addWidget(add_button)

    def populate_table(self, wear_rate_data):
        self.table_widget.clear()  # Clear existing contents
        self.table_widget.setColumnCount(len(wear_rate_data[0]) + 1)  # Add one column for delete button
        self.table_widget.setRowCount(len(wear_rate_data))
        headers = list(wear_rate_data[0].keys()) + ["Actions"]
        self.table_widget.setHorizontalHeaderLabels(headers)
        for row_index, row_data in enumerate(wear_rate_data):
            for col_index, key in enumerate(headers):
                if key != "Actions":
                    item = QTableWidgetItem(str(row_data[key]))
                    item.setFlags(Qt.ItemFlag.ItemIsEnabled)
                    self.table_widget.setItem(row_index, col_index, item)
                else:
                    delete_button = QPushButton("Delete")
                    delete_button.clicked.connect(lambda _, index=row_index: self.delete_record(index))
                    self.table_widget.setCellWidget(row_index, col_index, delete_button)

    def add_new_record_dialog(self):
        # Open a dialog to input data for the new wear rate record
        new_wear_rate_dialog = NewWearRateDialog(self.building_id)
        new_wear_rate_dialog.record_added.connect(self.refresh_table)
        new_wear_rate_dialog.exec()

    def delete_record(self, row_index):
        # Get the ID of the record to be deleted
        record_id_item = self.table_widget.item(row_index, 0)
        if record_id_item is None:
            return
        record_id = int(record_id_item.text())

        # Confirm deletion with a message box
        reply = QMessageBox.question(self, "Delete Record", "Are you sure you want to delete this record?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            # Delete the record from the database
            session = db_session()
            record_to_delete = session.query(WearRate).filter(WearRate.ID_wear_rate == record_id).first()
            session.delete(record_to_delete)
            session.commit()
            session.close()

            # Refresh the table
            self.refresh_table()

    def refresh_table(self):
        # Fetch updated data and refresh the table
        session = db_session()
        wear_rates = session.query(WearRate).filter(WearRate.ID_building == self.building_id).all()
        session.close()

        # Prepare data for the table
        wear_rate_data = []
        for rate in wear_rates:
            wear_rate_data.append({
                "ID": rate.ID_wear_rate,
                "Date": rate.date,
                "Wear Rate": rate.wear_rate_name
            })

        # Populate the table with updated data
        self.populate_table(wear_rate_data)