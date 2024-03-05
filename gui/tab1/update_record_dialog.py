from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QCompleter, QMessageBox, QGridLayout
)
from PyQt6.QtGui import QIntValidator, QDoubleValidator
from PyQt6.QtCore import QStringListModel
from database.models import Street, TypeConstruction, BasicProject, Appointment, LoadBearingWalls, \
    BuildingRoof, BuildingFloor, Facade, Foundation, ManagementCompany, BuildingDescription
from database.database import db_session
from constants import LABELS



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
            self.labels = LABELS
            grid_layout = QGridLayout()
            layout.addLayout(grid_layout)

            # Include 'street_name' in the required fields
            required_fields = ["street_name"]

            num_columns = 2  # Number of columns in the grid layout
            for idx, (label_text, value) in enumerate(self.record_data.items()):
                if label_text == "ID_street":
                    label_text = "street_name"  # Replace ID_street with street_name
                label = QLabel(label_text.replace('_', ' '))  # Replacing underscores with spaces for better readability
                line_edit = QLineEdit()

                # Add validator based on data type
                validator = None
                if label_text in ("house", "building_body", "cadastral_number", "year_construction", "number_floors",
                                "number_entrances", "number_buildings", "number_living_quarters", "cadastral_cost",
                                "year_overhaul", "Land_area"):
                    validator = QIntValidator()
                elif label_text in ("latitude", "longitude", "seismic_resistance_min", "seismic_resistance_max",
                                    "zone_SMZ_min", "zone_SMZ_max", "basement_area"):
                    validator = QDoubleValidator()

                if validator:
                    line_edit.setValidator(validator)

                # Add QCompleter if needed
                if label_text in ("street_name", "type_construction_name", "basic_project_name", "appointment_name",
                                    "load_bearing_walls_name", "building_roof_name", "building_floor_name", "facade_name",
                                    "foundation_name", "management_company_name"):
                    completer = QCompleter()
                    session = db_session()  # Assuming db_session is your SQLAlchemy session

                    query_classes = {
                        "street_name": Street.street_name,
                        "type_construction_name": TypeConstruction.type_construction_name,
                        "basic_project_name": BasicProject.basic_project_name,
                        "appointment_name": Appointment.appointment_name,
                        "load_bearing_walls_name": LoadBearingWalls.load_bearing_walls_name,
                        "building_roof_name": BuildingRoof.building_roof_name,
                        "building_floor_name": BuildingFloor.building_floor_name,
                        "facade_name": Facade.facade_name,
                        "foundation_name": Foundation.foundation_name,
                        "management_company_name": ManagementCompany.management_company_name
                    }

                    if label_text in query_classes:
                        data_query = session.query(query_classes[label_text]).distinct().all()

                    session.close()

                    data = [str(getattr(item, label_text)) for item in data_query]
                    model = QStringListModel(data)
                    completer.setModel(model)
                    line_edit.setCompleter(completer)

                # Prefill the line edit with existing data
                if value is not None:
                    line_edit.setText(str(value))

                # Adjusting layout for two columns
                row = idx // num_columns
                col = idx % num_columns * 2
                grid_layout.addWidget(label, row, col)  # Add the label to the grid
                grid_layout.addWidget(line_edit, row, col + 1)  # Add the line edit to the grid
                self.line_edits[label_text] = line_edit  # Store line edit in the dictionary


            # Ensure 'street_name' is in self.line_edits, if not add an empty QLineEdit
            if 'street_name' not in self.line_edits:
                self.line_edits['street_name'] = QLineEdit()

            save_button = QPushButton("Save")
            save_button.clicked.connect(self.update_record)
            layout.addWidget(save_button)
            
    def update_record(self):
        # Get updated data from the form fields
        updated_data = {}
        required_fields = ["street_name", "house"]  # Specify the required fields

        # Check if the required fields are empty
        for field in required_fields:
            if not self.line_edits.get(field):
                print(f"DEBUG: Field '{field}' not found in line edits.")
                QMessageBox.warning(self, "Warning", f"Please enter a value for {field}.")
                return

        for label_text, line_edit in self.line_edits.items():
            value = line_edit.text()
            if value:  # Check if the value is not empty
                updated_data[label_text] = value

        # Convert name values to ID values for applicable fields
        for label_text, _, related_model in self.labels:
            if label_text.startswith("ID_") and related_model:
                session = db_session()
                name_value = updated_data.get(label_text.replace("ID_", "") + "_name", "")
                if name_value:
                    # Query the related table to find the ID corresponding to the name value
                    related_instance = session.query(related_model).filter_by(**{related_model.__tablename__ + "_name": name_value}).first()
                    session.close()
                    if related_instance:
                        updated_data[label_text] = getattr(related_instance, "ID_" + related_model.__tablename__)
                    else:
                        QMessageBox.warning(self, "Warning", f"No matching record found for {name_value} in {related_model.__tablename__}.")
                        return

        print(f"\n\nUpdated data: {updated_data}\n\n")  # Debug print to check the updated data

        # Update the record in the database
        session = db_session()
        record_id = self.record_data.get("ID_building")
        record = session.query(BuildingDescription).filter_by(ID_building=record_id).first()

        if record:
            print(f"\n\nExisting record: {record.__dict__}\n\n")  # Debug print to check the existing record before update
            try:
                for key, value in updated_data.items():
                    if hasattr(record, key):
                        setattr(record, key, value)
                    else:
                        # If the key doesn't exist in the record, skip it
                        print(f"Warning: Key '{key}' not found in record.")
            except Exception as e:
                session.rollback()
                QMessageBox.warning(self, "Error", f"Failed to update record: {str(e)}")
                return

            try:
                session.commit()
                QMessageBox.information(self, "Success", "Record updated successfully.")
                self.close()
            except Exception as e:
                session.rollback()
                QMessageBox.warning(self, "Error", f"Failed to update record: {str(e)}")
        else:
            QMessageBox.warning(self, "Error", "Record not found.")

        session.close()

