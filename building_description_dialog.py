from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QGridLayout, QLabel, QLineEdit, QPushButton, QCompleter
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

        table_widget = QTableWidget()
        table_headers = ["street_name", "house", "building_body", "latitude", "longitude", "year_construction",
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
        header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

        # Populate the table with data
        for row_index, row_data in enumerate(data):
            table_widget.insertRow(row_index)
            for col_index, header in enumerate(table_headers):
                if hasattr(row_data, header):
                    cell_value = getattr(row_data, header)
                    if cell_value is not None:
                        cell_value = str(cell_value)
                    else:
                        cell_value = ""
                else:
                    # Handle the case where the attribute does not exist (not a direct column of BuildingDescription)
                    # Assume it's a foreign key and retrieve the related name
                    if header.endswith("_name"):
                        related_model_name = header.replace("_name", "")
                        related_instance = getattr(row_data, related_model_name, None)
                        if related_instance:
                            # Check if the attribute exists in the related model
                            cell_value = getattr(related_instance, related_model_name, "")
                        else:
                            cell_value = ""
                table_widget.setItem(row_index, col_index, QTableWidgetItem(cell_value))


        # Add the table widget to the dialog layout
        table_layout.addWidget(table_widget)

        # Show the dialog
        table_dialog.exec()
            
