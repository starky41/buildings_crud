from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QCompleter, QMessageBox, QGridLayout
)
from PyQt6.QtGui import QIntValidator, QDoubleValidator
from PyQt6.QtCore import QStringListModel


from database.models import BuildingDescription
from database.database import db_session
from constants import field_labels
from sqlalchemy.orm import joinedload
from constants import LABELS
from database.data_access_layer import DataAccessLayer


class AddRecordDialog(QDialog):
    def __init__(self, record_data=None):
        self.line_edits = {}  # Initialize line edits dictionary
        self.foreign_keys = {}  # Initialize dictionary to store foreign key name-value pairs
        super().__init__()
        self.setWindowTitle("Add Record")
        self.initUI()
        self.substituted_values = {}
        self.dal = DataAccessLayer(db_session())
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
        self.labels = LABELS

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
                name_value = data.get(label_text, "")  # Get the value or empty string if not present
                if name_value:
                    # Query the related table to find the ID corresponding to the name value
                    related_instance = self.dal.read(related_model, **{related_model.__tablename__ + "_name": name_value})
                    if related_instance:
                        data[label_text] = getattr(related_instance[0], "ID_" + related_model.__tablename__)
                    else:
                        QMessageBox.warning(self, "Warning", f"No matching record found for {name_value} in {related_model.__tablename__}.")
                        return

        # Create a new instance of BuildingDescription with the data
        new_building = BuildingDescription(**data)

        # Add the new record to the database
        try:
            self.dal.create(new_building)
            QMessageBox.information(self, "Success", "Record added successfully.")
            self.clear_fields()
            self.close()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to add record: {str(e)}")

    def clear_fields(self):
        for line_edit in self.line_edits.values():
            line_edit.clear()
