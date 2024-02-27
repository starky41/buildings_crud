from PyQt6.QtWidgets import QDialog, QLabel, QLineEdit, QVBoxLayout, QPushButton, QGridLayout
from PyQt6.QtGui import QIntValidator, QDoubleValidator

class AdditionalFieldsDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Record")
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.show_additional_fields(layout)  # Call the function to create fields
        layout.addWidget(QPushButton("Save"))  # Add a save button or any other buttons as needed

    def show_additional_fields(self, layout):
        labels = [
            ("ID_street", "int"), ("house", "int"), ("building_body", "int"),
            ("latitude", "numeric"), ("longitude", "numeric"), ("year_construction", "int"),
            ("number_floors", "int"), ("number_entrances", "int"), ("number_buildings", "int"),
            ("number_living_quarters", "int"), ("title", "VARCHAR(150)"), ("ID_type_construction", "INT"),
            ("ID_basic_project", "INT"), ("ID_appointment", "INT"), ("seismic_resistance_min", "NUMERIC"),
            ("seismic_resistance_max", "numeric"), ("zone_SMZ_min", "NUMERIC"), ("zone_SMZ_max", "numeric"),
            ("priming", "VARCHAR(150)"), ("ID_load_bearing_walls", "INT"), ("basement_area", "NUMERIC"),
            ("ID_building_roof", "INT"), ("ID_building_floor", "INT"), ("ID_facade", "INT"),
            ("ID_foundation", "INT"), ("azimuth", "VARCHAR(150)"), ("cadastral_number", "INT"),
            ("cadastral_cost", "NUMERIC"), ("year_overhaul", "INT"), ("accident_rate", "VARCHAR(150)"),
            ("ID_management_company", "INT"), ("Land_area", "Numeric"), ("notes", "VARCHAR(150)"),
            ("author", "VARCHAR(150)")
        ]

        # Create a QGridLayout
        grid_layout = QGridLayout()
        row = 0
        col = 0

        # Add labels and line edits to the grid layout
        for label_text, data_type in labels:
            label = QLabel(label_text)
            line_edit = QLineEdit()
            if data_type in ["int", "INT"]:
                line_edit.setValidator(QIntValidator())
            elif data_type in ["numeric", "NUMERIC"]:
                line_edit.setValidator(QDoubleValidator())
            else:  # Assume VARCHAR(150) or similar string types
                line_edit.setMaxLength(150)

            grid_layout.addWidget(label, row, col)
            grid_layout.addWidget(line_edit, row, col + 1)
            col += 2
            if col > 2:
                col = 0
                row += 1

        layout.addLayout(grid_layout)