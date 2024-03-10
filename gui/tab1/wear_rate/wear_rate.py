from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QMessageBox, QLineEdit, QTableWidgetItem
from PyQt6.QtCore import Qt, pyqtSignal
from datetime import date
from database.models import WearRate
from database.database import db_session
from gui.widgets.sortable_table_widget import SortableTableWidget


class WearRateDialog(QDialog):
    def __init__(self, wear_rate_data, building_id):
        super().__init__()
        self.setWindowTitle("Wear Rate")
        self.building_id = building_id
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.table_widget = SortableTableWidget()
        layout.addWidget(self.table_widget)

        # Check if wear rate data is available
        if wear_rate_data:
            self.populate_table(wear_rate_data)
        else:
            layout.addWidget(QLabel("No wear rate data available."))

        # Add button to add a new record
        add_button = QPushButton("Add New Record")
        add_button.clicked.connect(self.add_new_record_dialog)
        layout.addWidget(add_button)

    def populate_table(self, wear_rate_data):
        self.table_widget.clear()  # Clear existing contents
        if not wear_rate_data:
            layout = QVBoxLayout()
            self.setLayout(layout)
            layout.addWidget(QLabel("No wear rate data available."))
            return

        headers = list(wear_rate_data[0].keys()) + ["Actions", ""]
        self.table_widget.setColumnCount(len(headers))
        self.table_widget.setRowCount(len(wear_rate_data))
        self.table_widget.setHorizontalHeaderLabels(headers)

        for row_index, row_data in enumerate(wear_rate_data):
            for col_index, key in enumerate(headers):
                if key != "Actions":
                    item = QTableWidgetItem(str(row_data.get(key, "")))
                    item.setFlags(Qt.ItemFlag.ItemIsEnabled)
                    self.table_widget.setItem(row_index, col_index, item)
                elif key == "Actions":
                    edit_button = QPushButton("Edit")
                    edit_button.clicked.connect(lambda _, index=row_index: self.edit_record_dialog(index))
                    self.table_widget.setCellWidget(row_index, col_index, edit_button)

                    delete_button = QPushButton("Delete")
                    delete_button.clicked.connect(lambda _, index=row_index: self.delete_record(index))
                    self.table_widget.setCellWidget(row_index, col_index + 1, delete_button)


    def add_new_record_dialog(self):
        # Open a dialog to input data for the new wear rate record
        new_wear_rate_dialog = NewWearRateDialog(self.building_id)
        new_wear_rate_dialog.record_added.connect(self.refresh_table)
        new_wear_rate_dialog.exec()

    def edit_record_dialog(self, row_index):
        # Get data for the selected record
        record_id_item = self.table_widget.item(row_index, 0)
        if record_id_item is None:
            return
        record_id = int(record_id_item.text())
        date_item = self.table_widget.item(row_index, 1).text()
        wear_rate_name = self.table_widget.item(row_index, 2).text()

        # Open a dialog to edit the selected record
        edit_wear_rate_dialog = EditWearRateDialog(record_id, date_item, wear_rate_name)
        edit_wear_rate_dialog.record_updated.connect(self.refresh_table)
        edit_wear_rate_dialog.exec()

    def delete_record(self, row_index):
        # Get the ID of the record to be deleted
        record_id_item = self.table_widget.item(row_index, 0)
        if record_id_item is None:
            return
        record_id = int(record_id_item.text())

        # Confirm deletion with a message box
        reply = QMessageBox.question(self, "Delete Record", "Are you sure you want to delete this record?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            # Delete the record from the database
            session = db_session()
            record_to_delete = session.query(WearRate).filter(WearRate.ID_wear_rate == record_id).first()
            session.delete(record_to_delete)
            session.commit()
            session.close()

            # Refresh the table
            self.refresh_table()

    def refresh_table(self):
        # Fetch updated data and refresh the table
        session = db_session()
        wear_rates = session.query(WearRate).filter(WearRate.ID_building == self.building_id).all()
        session.close()

        # Prepare data for the table
        wear_rate_data = []
        for rate in wear_rates:
            wear_rate_data.append({
                "ID": rate.ID_wear_rate,
                "Date": rate.date,
                "Wear Rate": rate.wear_rate_name
            })

        # Populate the table with updated data
        self.populate_table(wear_rate_data)

class BaseWearRateDialog(QDialog):
    record_updated = pyqtSignal()
    record_added = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Input fields for date and wear rate name
        self.date_input = QLineEdit()
        self.date_input.setPlaceholderText("Date (YYYY-MM-DD)")
        layout.addWidget(self.date_input)

        self.wear_rate_name_input = QLineEdit()
        self.wear_rate_name_input.setPlaceholderText("Wear Rate Name")
        layout.addWidget(self.wear_rate_name_input)

        # Add button to confirm action
        if isinstance(self, EditWearRateDialog):
            button_text = "Edit"
            self.action_function = self.edit_record
        elif isinstance(self, NewWearRateDialog):
            button_text = "Add"
            self.action_function = self.add_new_record

        action_button = QPushButton(button_text)
        action_button.clicked.connect(self.action_function)
        layout.addWidget(action_button)

    def validate_input(self, date_str, wear_rate_name):
        if not date_str or not wear_rate_name:
            QMessageBox.warning(self, "Warning", "Please fill in all fields.")
            return False

        try:
            date.fromisoformat(date_str)
        except ValueError:
            QMessageBox.warning(self, "Error", "Invalid date format. Please use YYYY-MM-DD.")
            return False

        return True

    def edit_record(self):
        date_str = self.date_input.text()
        wear_rate_name = self.wear_rate_name_input.text()

        if not self.validate_input(date_str, wear_rate_name):
            return

        # Update the wear rate record
        session = db_session()
        record_to_update = session.query(WearRate).filter(WearRate.ID_wear_rate == self.record_id).first()
        record_to_update.date = date.fromisoformat(date_str)
        record_to_update.wear_rate_name = wear_rate_name
        session.commit()
        session.close()

        self.record_updated.emit()
        self.accept()

    def add_new_record(self):
        date_str = self.date_input.text()
        wear_rate_name = self.wear_rate_name_input.text()

        if not self.validate_input(date_str, wear_rate_name):
            return

        new_wear_rate = WearRate(date=date.fromisoformat(date_str), wear_rate_name=wear_rate_name, ID_building=self.building_id)

        # Add the new record to the database
        session = db_session()
        session.add(new_wear_rate)
        session.commit()
        session.close()

        self.record_added.emit()
        self.accept()

class EditWearRateDialog(BaseWearRateDialog):
    def __init__(self, record_id, date, wear_rate_name):
        super().__init__()
        self.setWindowTitle("Edit Wear Rate Record")
        self.record_id = record_id
        self.date_input.setText(date)
        self.wear_rate_name_input.setText(wear_rate_name)

class NewWearRateDialog(BaseWearRateDialog):
    def __init__(self, building_id):
        super().__init__()
        self.setWindowTitle("Add New Wear Rate Record")
        self.building_id = building_id
