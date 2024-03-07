from database.crud_operations import CrudOperations
from database.get_model_class import get_model_class
from database.database import engine
from PyQt6.QtWidgets import QTableWidgetItem
class WearRateCrudOperations(CrudOperations):
    def refreshTable(self, model_class_name, table_widget, addUpdateButton, selected_row):
        model_class = get_model_class(model_class_name)
        if model_class:
            # Clear existing data in the table widget
            table_widget.clear()

            # Fetch data from the database table where ID_building matches the selected row
            with engine.connect() as connection:
                result = connection.execute(model_class.__table__.select().where(model_class.__table__.c.ID_building == selected_row))
                rows = result.fetchall()

            # Set the table dimensions based on the retrieved data
            table_widget.setRowCount(len(rows))
            table_widget.setColumnCount(len(model_class.__table__.columns))

            # Populate the table with the fetched data
            for row_idx, row in enumerate(rows):
                for col_idx, col in enumerate(row):
                    item = QTableWidgetItem(str(col))
                    table_widget.setItem(row_idx, col_idx, item)
                addUpdateButton(self, row_idx, table_widget, model_class_name, addUpdateButton)

            # Set table headers
            headers = [str(col) for col in model_class.__table__.columns.keys()]
            table_widget.setHorizontalHeaderLabels(headers)
