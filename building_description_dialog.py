from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QGridLayout, QLabel, QLineEdit, QPushButton, QCompleter, QMessageBox
)
from PyQt6.QtGui import QIntValidator, QDoubleValidator
from sqlalchemy.orm import sessionmaker
from models import Street, TypeConstruction, BasicProject, Appointment, LoadBearingWalls, \
    BuildingRoof, BuildingFloor, Facade, Foundation, ManagementCompany, BuildingDescription
from PyQt6.QtCore import QStringListModel
from database import db_session
from data_access_layer import DataAccessLayer
from sqlalchemy.exc import IntegrityError
from sqlalchemy import inspect
from constants import field_labels
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView
from sqlalchemy.orm import joinedload
from PyQt6.QtCore import Qt

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

class BuildingDescriptionDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Record")
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.line_edits = {}  # Initialize a dictionary to store line edits
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

        self.view_table_button = QPushButton("View Table")
        self.view_table_button.clicked.connect(self.view_table)
        layout.addWidget(self.view_table_button)

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

        # Clear line edits
        for line_edit in self.line_edits.values():
            line_edit.clear()

        # Optionally, refresh the table or perform any other necessary actions
        print("New record added successfully!")
    def view_table(self):
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

        # Create a new dialog to display the table
        table_dialog = QDialog(self)
        table_layout = QVBoxLayout()
        table_dialog.setLayout(table_layout)

        table_widget = SortableTableWidget()
        table_headers = ["ID_building", "street_name", "house", "building_body", "latitude", "longitude", "year_construction",
                        "number_floors", "number_entrances", "number_buildings", "number_living_quarters",
                        "title", "type_construction_name", "basic_project_name", "appointment_name",
                        "seismic_resistance_min", "seismic_resistance_max", "zone_SMZ_min", "zone_SMZ_max",
                        "priming", "load_bearing_walls_name", "basement_area", "building_roof_name",
                        "building_floor_name", "facade_name", "foundation_name", "azimuth", "cadastral_number",
                        "cadastral_cost", "year_overhaul", "accident_rate", "management_company_name",
                        "Land_area", "notes", "author"]
        table_widget.setColumnCount(len(table_headers))
        table_widget.setHorizontalHeaderLabels(table_headers)

        # Adjusting header size to contents
        header = table_widget.horizontalHeader()
        header.ResizeMode(QHeaderView.ResizeMode.ResizeToContents)

        # Populate the table with data
        for row_index, row_data in enumerate(data):
            table_widget.insertRow(row_index)
            for col_index, header in enumerate(table_headers):
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
                table_widget.setItem(row_index, col_index, QTableWidgetItem(str(cell_value)))

        # Add the table widget to the dialog layout
        table_layout.addWidget(table_widget)

        # Add a delete button below the table
        delete_button = QPushButton("Delete Selected Record")
        delete_button.clicked.connect(lambda: self.delete_selected_record(table_widget))
        table_layout.addWidget(delete_button)

        # Add an update button below the table
        update_button = QPushButton("Update Selected Record")
        update_button.clicked.connect(lambda: self.update_record(table_widget))
        table_layout.addWidget(update_button)

        # Show the dialog
        table_dialog.show()

    def delete_selected_record(self, table_widget):
        selected_rows = table_widget.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "Warning", "Please select a record to delete.")
            return

        # Assuming only one row can be selected at a time
        row_index = selected_rows[0].row()
        cell_text = table_widget.item(row_index, 0).text()  # Assuming the first column contains the primary key
        print("Cell Text:", cell_text)  # Add this line for debugging
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
            table_widget.removeRow(row_index)
            QMessageBox.information(self, "Success", "Record deleted successfully.")
        else:
            QMessageBox.warning(self, "Warning", "Record not found.")


    def populate_table(self, table_widget):
        table_headers = ["street_name", "house", "building_body", "latitude", "longitude", "year_construction",
                "number_floors", "number_entrances", "number_buildings", "number_living_quarters",
                "title", "type_construction_name", "basic_project_name", "appointment_name",
                "seismic_resistance_min", "seismic_resistance_max", "zone_SMZ_min", "zone_SMZ_max",
                "priming", "load_bearing_walls_name", "basement_area", "building_roof_name",
                "building_floor_name", "facade_name", "foundation_name", "azimuth", "cadastral_number",
                "cadastral_cost", "year_overhaul", "accident_rate", "management_company_name",
                "Land_area", "notes", "author", "actions"]

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

        # Populate the table with data
        for row_index, row_data in enumerate(data):
            table_widget.insertRow(row_index)
            for col_index, header in enumerate(table_headers):
                cell_value = ""
                if header == "actions":
                    # Create a delete button for each row
                    delete_button = QPushButton("Delete")
                    delete_button.clicked.connect(lambda _, r=row_data, tw=table_widget: self.delete_record(r, tw))

                    table_widget.setCellWidget(row_index, col_index, delete_button)
                elif hasattr(row_data, header):
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
                    table_widget.setItem(row_index, col_index, QTableWidgetItem(str(cell_value)))

    def update_record(self, table_widget):
        # Fetch selected record's data
        selected_rows = table_widget.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "Warning", "Please select a record to update.")
            return

        row_index = selected_rows[0].row()
        record_id = int(table_widget.item(row_index, 0).text())

        session = db_session()
        record = session.query(BuildingDescription).get(record_id)
        if not record:
            QMessageBox.warning(self, "Warning", "Record not found.")
            return

        # Populate dialog fields with existing data
        for label_text, _, related_model in self.labels:
            line_edit = self.line_edits[label_text]
            if label_text.startswith("ID_") and related_model:
                # If it's a foreign key, load the name instead of the ID
                related_instance = getattr(record, label_text[3:].lower())
                if related_instance:
                    line_edit.setText(getattr(related_instance, label_text[3:].lower() + "_name", ""))
            else:
                # Otherwise, load the data directly
                value = getattr(record, label_text, None)
                if value is not None:
                    line_edit.setText(str(value))
                else:
                    line_edit.clear()

        # Open the dialog for editing
        self.exec()

        # Update the record with edited data
        for label_text, _, related_model in self.labels:
            line_edit = self.line_edits[label_text]
            value = line_edit.text()
            if label_text.startswith("ID_") and related_model:
                # If it's a foreign key, convert the name to ID
                name_value = value
                if name_value:  # Check if value is not an empty string
                    related_instance = session.query(related_model).filter_by(**{related_model.__tablename__ + "_name": name_value}).first()
                    if related_instance:
                        # Use the primary key attribute of the related object
                        if label_text == "ID_type_construction":
                            setattr(record, label_text, related_instance.ID_type_construction)  # Adjust with the correct attribute
                        
                        elif label_text == "ID_type_construction":
                            setattr(record, label_text, related_instance.ID_type_construction)  # Adjust with the correct attribute
                        elif label_text == "ID_basic_project":
                            setattr(record, label_text, related_instance.ID_basic_project)  # Adjust with the correct attribute
                        elif label_text == "ID_appointment":
                            setattr(record, label_text, related_instance.ID_appointment)  # Adjust with the correct attribute
                        elif label_text == "ID_load_bearing_walls":
                            setattr(record, label_text, related_instance.ID_load_bearing_walls)  # Adjust with the correct attribute
                        elif label_text == "ID_building_roof":
                            setattr(record, label_text, related_instance.ID_building_roof)  # Adjust with the correct attribute
                        # Add more conditions for other related models as needed
                        elif label_text == "ID_building_floor":
                            setattr(record, label_text, related_instance.ID_building_floor)  # Adjust with the correct attribute
                        elif label_text == "ID_facade":
                            setattr(record, label_text, related_instance.ID_facade)  # Adjust with the correct attribute
                        elif label_text == "ID_management_company":
                            setattr(record, label_text, related_instance.ID_management_company)  # Adjust with the correct attribute
                else:
                    setattr(record, label_text, None)  # Set to None if value is empty
            elif value != '':  # Check if value is not an empty string
                setattr(record, label_text, value)
            else:
                setattr(record, label_text, None)  # Set to None if value is empty

        session.commit()
        session.close()

        # Optionally, refresh the table or perform any other necessary actions
        print("Record updated successfully!")

