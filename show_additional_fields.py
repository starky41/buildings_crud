from PyQt6.QtWidgets import QLabel, QLineEdit, QGridLayout
from PyQt6.QtGui import QIntValidator, QDoubleValidator
def show_additional_fields(self, visibility):
    if not hasattr(self, 'fields_created'):
        self.fields_created = False

    if visibility and not self.fields_created:
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

        # Clear the second section and add the text fields
        for widget in getattr(self, 'section2Widgets', []):
            self.section2.removeWidget(widget)
            widget.deleteLater()

        # Create a GridLayout
        grid_layout = QGridLayout()
        self.textFields = []

        # Add labels and line edits to the grid layout
        for row, (label_text, data_type) in enumerate(labels):
            label = QLabel(label_text)
            if data_type in ["int", "INT"]:
                line_edit = QLineEdit()
                line_edit.setValidator(QIntValidator())
            elif data_type in ["numeric", "NUMERIC"]:
                line_edit = QLineEdit()
                line_edit.setValidator(QDoubleValidator())
            else:  # Assume VARCHAR(150) or similar string types
                line_edit = QLineEdit()
                line_edit.setMaxLength(150)

            # Determine the column by taking the row modulus 2 (for 2 columns)
            column = row % 2
            # Calculate the grid row by integer dividing the label index by 2
            grid_row = row // 2

            grid_layout.addWidget(label, grid_row, column * 2)  # Multiply by 2 for alternating columns
            grid_layout.addWidget(line_edit, grid_row, column * 2 + 1)

            self.textFields.append(line_edit)

        self.section2.addLayout(grid_layout)
        self.fields_created = True

    self.section2Wrapper.setVisible(visibility)