from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QGridLayout, QLabel, QLineEdit, QPushButton, QCompleter
)
from PyQt6.QtGui import QIntValidator, QDoubleValidator
from sqlalchemy.orm import sessionmaker
from models import Street, TypeConstruction, BasicProject, Appointment, LoadBearingWalls, \
    BuildingRoof, BuildingFloor, Facade, Foundation, ManagementCompany
from PyQt6.QtCore import QStringListModel
from database import db_session

class BuildingDescriptionDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Record")
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.show_bd_fields(layout)  # Call the function to create fields
        layout.addWidget(QPushButton("Save"))  # Add a save button or any other buttons as needed

    def show_bd_fields(self, layout):
        labels = [
            ("ID_street", "int", Street), ("house", "int", None), ("building_body", "int", None),
            ("latitude", "numeric", None), ("longitude", "numeric", None), ("year_construction", "int", None),
            ("number_floors", "int", None), ("number_entrances", "int", None), ("number_buildings", "int", None),
            ("number_living_quarters", "int", None), ("title", "varchar", None), 
            ("ID_type_construction", "int", TypeConstruction), ("ID_basic_project", "int", BasicProject), 
            ("ID_appointment", "int", Appointment), ("seismic_resistance_min", "numeric", None),
            ("seismic_resistance_max", "numeric", None), ("zone_SMZ_min", "numeric", None), 
            ("zone_SMZ_max", "numeric", None), ("priming", "varchar", None), 
            ("ID_load_bearing_walls", "int", LoadBearingWalls), ("basement_area", "numeric", None),
            ("ID_building_roof", "int", BuildingRoof), ("ID_building_floor", "int", BuildingFloor), 
            ("ID_facade", "int", Facade), ("ID_foundation", "int", Foundation), 
            ("azimuth", "varchar", None), ("cadastral_number", "int", None),
            ("cadastral_cost", "numeric", None), ("year_overhaul", "int", None), 
            ("accident_rate", "varchar", None), ("ID_management_company", "int", ManagementCompany), 
            ("Land_area", "numeric", None), ("notes", "varchar", None), 
            ("author", "varchar", None)
        ]

        # Create a QGridLayout
        grid_layout = QGridLayout()
        row = 0
        col = 0

        # Add labels and line edits to the grid layout
        for label_text, data_type, related_model in labels:
            label = QLabel(label_text)
            line_edit = QLineEdit()
            completer = QCompleter()
            line_edit.setCompleter(completer)

            grid_layout.addWidget(label, row, col)
            grid_layout.addWidget(line_edit, row, col + 1)
            col += 2
            if col > 2:
                col = 0
                row += 1

            # If it's a foreign key field, set up autocompletion based on data from related table
            if related_model:
                session = db_session()
                data = session.query(related_model).all()
                session.close()

                # Get the primary key attribute name of the related model
                pk_attribute = getattr(related_model, '__table__').primary_key.columns.values()[0].name

                # Get a list of primary key values
                pk_values = [str(getattr(item, pk_attribute)) for item in data]

                # Create a QStringListModel and set it as the model for the completer
                completer_model = QStringListModel(pk_values)
                completer.setModel(completer_model)
            else:
                # Add validators for fields where applicable
                if "int" in data_type:
                    line_edit.setValidator(QIntValidator())
                elif "numeric" in data_type:
                    line_edit.setValidator(QDoubleValidator())

        layout.addLayout(grid_layout)