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

    def show_bd_fields(self, layout):
        # Create a QGridLayout
        grid_layout = QGridLayout()
        row = 0
        col = 0

        # Add labels and line edits to the grid layout
        for label_text, data_type, _ in self.labels:
            label = QLabel(label_text)
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

        # Optionally, refresh the table or perform any other necessary actions
        print("New record added successfully!")