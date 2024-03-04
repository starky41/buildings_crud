from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QCompleter, QMessageBox,
    QHBoxLayout, QGridLayout, QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt6.QtGui import QIntValidator, QDoubleValidator
from PyQt6.QtCore import QStringListModel, Qt
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from sqlalchemy.orm import sessionmaker
from models import Street, TypeConstruction, BasicProject, Appointment, LoadBearingWalls, \
    BuildingRoof, BuildingFloor, Facade, Foundation, ManagementCompany, BuildingDescription
from database import db_session
from constants import field_labels
from sqlalchemy.orm import joinedload

class SortableTableWidget(QTableWidget):
    def __init__(self):
        super().__init__()

        # Connect the header clicked signal to the sorting function
        self.horizontalHeader().sectionClicked.connect(self.sort_column)
        self.last_sorted_column = None
        self.sort_order = Qt.SortOrder.AscendingOrder

    def sort_column(self, logical_index):
        # If the same column header is clicked, toggle the sort order
        if logical_index == self.last_sorted_column:
            self.sort_order = Qt.SortOrder.DescendingOrder if self.sort_order == Qt.SortOrder.AscendingOrder else Qt.SortOrder.AscendingOrder
        else:
            self.last_sorted_column = logical_index
            self.sort_order = Qt.SortOrder.AscendingOrder

        # Sort the table by the clicked column
        self.sortItems(logical_index, self.sort_order)
class UpdateRecordDialog(QDialog):
    def __init__(self, record_data):
        super().__init__()
        self.setWindowTitle("Update Record")
        self.record_data = record_data
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.line_edits = {}  # Initialize a dictionary to store line edits

        grid_layout = QGridLayout()
        layout.addLayout(grid_layout)

        for idx, (label_text, value) in enumerate(self.record_data.items()):
            label = QLabel(label_text.replace('_', ' '))  # Replacing underscores with spaces for better readability
            line_edit = QLineEdit(str(value))
            
            # Add validator based on data type
            if label_text == "house" or label_text == "building_body" or label_text == "cadastral_number" or label_text == "year_construction" or label_text == "number_floors" or label_text == "number_entrances" or label_text == "number_buildings" or label_text == "number_living_quarters" or label_text == "cadastral_cost" or label_text == "year_overhaul" or label_text == "Land_area":
                line_edit.setValidator(QIntValidator())
            elif label_text == "latitude" or label_text == "longitude" or label_text == "seismic_resistance_min" or label_text == "seismic_resistance_max" or label_text == "zone_SMZ_min" or label_text == "zone_SMZ_max" or label_text == "basement_area":
                line_edit.setValidator(QDoubleValidator())
            
            # Add QCompleter if needed
            if label_text == "ID_street" or label_text == "title" or label_text == "ID_type_construction" or label_text == "ID_basic_project" or label_text == "ID_appointment" or label_text == "ID_load_bearing_walls" or label_text == "ID_building_roof" or label_text == "ID_building_floor" or label_text == "ID_facade" or label_text == "ID_foundation" or label_text == "ID_management_company":
                completer = QCompleter()
                if hasattr(value, 'query'):
                    data = [str(item) for item in value.query.all()]
                else:
                    data = [value]

                model = QStandardItemModel()
                for item in data:
                    model.appendRow(QStandardItem(item))
                completer.setModel(model)
                line_edit.setCompleter(completer)

            grid_layout.addWidget(label, idx // 2, idx % 2 * 2)  # Add the label and line edit to the grid
            grid_layout.addWidget(line_edit, idx // 2, idx % 2 * 2 + 1)
            self.line_edits[label_text] = line_edit  # Store line edit in the dictionary

            # If line edit is empty, set it to an empty string instead of "None"
            if not value:
                line_edit.setText("")

        save_button = QPushButton("Save")
        save_button.clicked.connect(self.update_record)
        layout.addWidget(save_button)

    def update_record(self):
        # Get updated data from the form fields
        updated_data = {}

        for label_text, line_edit in self.line_edits.items():
            value = line_edit.text()
            # Convert empty strings to None
            if value == '':
                updated_data[label_text] = None
            else:
                updated_data[label_text] = value

        # Update the record in the database
        session = db_session()
        record_id = self.record_data.get("ID_building")  
        record = session.query(BuildingDescription).filter_by(ID_building=record_id).first()
        if record:
            for key, value in updated_data.items():
                setattr(record, key, value)
            session.commit()
            QMessageBox.information(self, "Success", "Record updated successfully.")
            self.close()
        else:
            QMessageBox.warning(self, "Error", "Record not found.")
        session.close()





class AddRecordDialog(QDialog):
    def __init__(self, record_data=None):
        self.line_edits = {}  # Initialize line edits dictionary
        self.foreign_keys = {}  # Initialize dictionary to store foreign key name-value pairs
        super().__init__()
        self.setWindowTitle("Add Record")
        self.initUI()
        self.record_data = record_data 
        # If record_data is provided, pre-fill the fields with its values
        if record_data:
            for label_text, line_edit in self.line_edits.items():
                if label_text in record_data:
                    line_edit.setText(str(record_data[label_text]))
            # Pre-fill foreign key fields
            for fk_label, fk_value in self.foreign_keys.items():
                self.line_edits[fk_label].setText(fk_value)

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.labels = [  # Store labels and their respective data types
            ("ID_street", "VARCHAR(150)", Street), ("house", "int", None), ("building_body", "int", None),
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
        ]

        self.show_bd_fields(layout)  # Call the function to create fields
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_record)  # Connect save_record method to clicked signal
        layout.addWidget(self.save_button)  # Add a save button or any other buttons as needed

    def show_bd_fields(self, layout):
        # Create a QGridLayout
        grid_layout = QGridLayout()
        row = 0
        col = 0

        # Add labels and line edits to the grid layout
        for label_text, data_type, _ in self.labels:
            label = QLabel(field_labels.get(label_text, label_text).replace('_', ' '))  # Replacing underscores with spaces for better readability
            line_edit = QLineEdit()
            completer = QCompleter()
            line_edit.setCompleter(completer)

            grid_layout.addWidget(label, row, col)
            grid_layout.addWidget(line_edit, row, col + 1)
            self.line_edits[label_text] = line_edit  # Store line edit in the dictionary
            col += 2
            if col > 2:
                col = 0
                row += 1

            # If it's a foreign key field, set up autocompletion based on data from related table
            if data_type.startswith("VARCHAR") or data_type.startswith("int"):
                related_model = None
                if data_type.startswith("VARCHAR"):
                    related_model = _  # Assign related model if applicable
                elif data_type.startswith("int"):
                    related_model = None  # No related model for integers
                if related_model:
                    session = db_session()
                    data = session.query(related_model).all()
                    session.close()

                    # Get the name attribute of the related model
                    name_attribute = label_text[3:] + "_name"
                    name_values = [str(getattr(item, name_attribute)) for item in data]

                    # Create a QStringListModel and set it as the model for the completer
                    completer_model = QStringListModel(name_values)
                    completer.setModel(completer_model)

                    # Store foreign key name-value pairs
                    for item in data:
                        self.foreign_keys[label_text] = str(getattr(item, name_attribute))
            else:
                # Add validators for fields where applicable
                if "int" in data_type:
                    line_edit.setValidator(QIntValidator())
                elif "numeric" in data_type:
                    line_edit.setValidator(QDoubleValidator())

        layout.addLayout(grid_layout)

    def save_record(self):
        # Get data from the form fields
        data = {}
        required_fields = ["ID_street", "house"]  # Specify the required fields

        # Check if the required fields are empty
        for field in required_fields:
            if not self.line_edits[field].text():
                QMessageBox.warning(self, "Warning", f"Please enter a value for {field}.")
                return

        for label_text, _, _ in self.labels:
            line_edit = self.line_edits[label_text]
            value = line_edit.text()
            if value:  # Check if the value is not empty
                data[label_text] = value

        # Convert name values to ID values
        for label_text, data_type, related_model in self.labels:
            if label_text.startswith("ID_") and related_model:
                session = db_session()
                name_value = data.get(label_text, "")  # Get the value or empty string if not present
                if name_value:
                    # Query the related table to find the ID corresponding to the name value
                    related_instance = session.query(related_model).filter_by(**{related_model.__tablename__ + "_name": name_value}).first()
                    session.close()
                    if related_instance:
                        data[label_text] = getattr(related_instance, "ID_" + related_model.__tablename__)
                    else:
                        QMessageBox.warning(self, "Warning", f"No matching record found for {name_value} in {related_model.__tablename__}.")
                        return

        # Create a new instance of BuildingDescription with the data
        new_building = BuildingDescription(**data)

        # Add the new record to the database
        session = db_session()
        session.add(new_building)
        session.commit()
        session.close()

        QMessageBox.information(self, "Success", "Record added successfully.")
        self.clear_fields()
        self.close()

    def clear_fields(self):
        for line_edit in self.line_edits.values():
            line_edit.clear()


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

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(len(self.table_headers))
        self.table_widget.setHorizontalHeaderLabels(self.table_headers)
        layout.addWidget(self.table_widget)

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

        session = db_session()
        record = session.query(BuildingDescription).get(record_id)
        if record:
            session.delete(record)
            session.commit()
            session.close()
            # Remove the row from the table
            self.table_widget.removeRow(row_index)
            QMessageBox.information(self, "Success", "Record deleted successfully.")
        else:
            QMessageBox.warning(self, "Warning", "Record not found.")
