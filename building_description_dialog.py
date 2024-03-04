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
        self.sortByColumn(logical_index, self.sort_order)
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

                    # Fetch data using joinedloads or relationships
                    if label_text == "street_name":
                        data_query = session.query(Street.street_name).distinct().all()
                    elif label_text == "type_construction_name":
                        data_query = session.query(TypeConstruction.type_construction_name).distinct().all()
                    elif label_text == "basic_project_name":
                        data_query = session.query(BasicProject.basic_project_name).distinct().all()
                    elif label_text == "appointment_name":
                        data_query = session.query(Appointment.appointment_name).distinct().all()
                    elif label_text == "load_bearing_walls_name":
                        data_query = session.query(LoadBearingWalls.load_bearing_walls_name).distinct().all()
                    elif label_text == "building_roof_name":
                        data_query = session.query(BuildingRoof.building_roof_name).distinct().all()
                    elif label_text == "building_floor_name":
                        data_query = session.query(BuildingFloor.building_floor_name).distinct().all()
                    elif label_text == "facade_name":
                        data_query = session.query(Facade.facade_name).distinct().all()
                    elif label_text == "foundation_name":
                        data_query = session.query(Foundation.foundation_name).distinct().all()
                    elif label_text == "management_company_name":
                        data_query = session.query(ManagementCompany.management_company_name).distinct().all()

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
