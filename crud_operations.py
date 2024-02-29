from sqlalchemy import inspect
from sqlalchemy.exc import IntegrityError
from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem, QPushButton, QDialog, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QFormLayout, QGridLayout
from data_access_layer import DataAccessLayer
from database import engine, db_session
from get_model_class import get_model_class
from models import Street
class CrudOperations:

    def createItem(self, model_class_name, db_session, DataAccessLayer, refreshTable, clearLineEdits, table_widget, addUpdateButton, layout):
        model_class = get_model_class(model_class_name)
        if model_class:
            inspector = inspect(model_class)
            columns = [column.name for column in inspector.columns]
            try:
                data = self.getFormData(columns=columns, model_class=model_class, layout=layout)
                new_instance = model_class(**data)
                dal = DataAccessLayer(db_session)
                dal.create(new_instance)
            except ValueError as e:
                self.showErrorDialog(str(e))
                db_session.rollback()
            except IntegrityError:
                self.showErrorDialog("The value already exists in the database")
                db_session.rollback()
            else:
                refreshTable(self, model_class_name, table_widget, addUpdateButton)
                clearLineEdits(self, columns, layout)
    
    def refreshTable(self, model_class_name, table_widget, addUpdateButton):
        model_class = get_model_class(model_class_name)
        if model_class:
            # Clear existing data in the table widget
            table_widget.clear()

            # Fetch data from the database table
            if model_class_name == 'BuildingDescription':
                # Fetch data with a join on Street table to get street_name
                query = db_session.query(model_class, Street.street_name).join(Street)
                rows = query.all()
            else:
                # For other tables, fetch data without a join
                with engine.connect() as connection:
                    result = connection.execute(model_class.__table__.select())
                    rows = result.fetchall()

            # Set the table dimensions based on the retrieved data
            if rows:
                table_widget.setRowCount(len(rows))

                # Determine the column count and headers
                headers = []
                column_count = 0

                for col in model_class.__table__.columns:
                    if col.key != 'ID_street':  # Exclude ID_street column
                        if col.key == 'ID_building':
                            headers.append('ID_building')
                            column_count += 1
                        elif col.key != 'ID_building' and col.key != 'street_name':
                            headers.append(col.key)
                            column_count += 1

                if model_class_name == 'BuildingDescription':
                    # For BuildingDescription, add street_name column after ID_building
                    headers.insert(headers.index('ID_building') + 1, 'street_name')
                    column_count += 1

                table_widget.setColumnCount(column_count)

                # Populate the table with the fetched data
                for row_idx, row in enumerate(rows):
                    if model_class_name == 'BuildingDescription':
                        # Extract data from the row
                        building_description, street_name = row

                        # Set columns for building description data
                        col_idx = 0
                        for col in model_class.__table__.columns:
                            if col.key != 'ID_street':  # Exclude ID_street column
                                if col.key == 'ID_building':
                                    item = QTableWidgetItem(str(getattr(building_description, col.key)))
                                    table_widget.setItem(row_idx, col_idx, item)
                                    col_idx += 1

                                    # Insert street_name column after ID_building
                                    street_item = QTableWidgetItem(str(street_name) if street_name is not None else '')
                                    table_widget.setItem(row_idx, col_idx, street_item)
                                    col_idx += 1
                                elif col.key != 'ID_building' and col.key != 'street_name':
                                    item = QTableWidgetItem(str(getattr(building_description, col.key)) if getattr(building_description, col.key) is not None else '')
                                    table_widget.setItem(row_idx, col_idx, item)
                                    col_idx += 1

                    else:
                        # For other tables, directly populate the table with row data
                        for col_idx, col in enumerate(row):
                            item = QTableWidgetItem(str(col) if col is not None else '')
                            table_widget.setItem(row_idx, col_idx, item)

                    # Add update button if required
                    addUpdateButton(self, row_idx, table_widget, model_class_name, addUpdateButton)

                # Set table headers
                table_widget.setHorizontalHeaderLabels(headers)



    def addUpdateButton(self, row_idx, table_widget, model_class_name, addUpdateButton):
        
        selected_row_index = table_widget.currentRow()
        if selected_row_index != -1:
            model_class = get_model_class(model_class_name)
            if model_class:
                primary_key_columns = [col.name for col in model_class.__table__.primary_key]
                row_data = [table_widget.item(selected_row_index, col).text() for col in range(table_widget.columnCount())]
                identifier = {col: val for col, val in zip(primary_key_columns, row_data)}
                # Assuming there is a method to get a form or dialog to edit the selected item
                edit_dialog = self.getEditDialog(model_class, identifier)
                if edit_dialog.exec():
                    dal = DataAccessLayer(db_session)
                    updated_data = edit_dialog.getUpdatedData()
                    dal.update(model_class, identifier, updated_data)
                    self.refreshTable(self, model_class_name, get_model_class, table_widget, addUpdateButton)
            else:
                QMessageBox.warning(self, "No selection", "Please select a row to edit.")
                update_button = QPushButton("Update")
                update_button.clicked.connect(lambda: self.updateItem(row_idx))
                table_widget.setCellWidget(row_idx, table_widget.columnCount(), update_button)


    def handleUpdateButtonClick(self, updateItem, model_class_name, table_widget):
        current_row = self.table_widget.currentRow()
        id_item = self.table_widget.item(current_row, 0)  # Assuming the first column is the ID
        if id_item is not None:
            updateItem(self, id_item.text(), model_class_name, table_widget)
        else:
            QMessageBox.warning(self, "Update Error", "Please select a valid row before updating.")



    def updateItem(self, id_value, model_class_name, table_widget):
        model_class = get_model_class(model_class_name)
        if model_class:
            dal = DataAccessLayer(db_session)
            
            primary_key_column = None
            editable_columns = []
            column_names = [col.name for col in model_class.__table__.columns]
            
            # Find the primary key and editable columns by excluding autoincrement and primary key columns
            for column in model_class.__table__.columns:
                if not column.primary_key or not column.autoincrement:
                    if column.name != "ID_" + model_class.__tablename__:
                        editable_columns.append(column.name)
                if column.primary_key:
                    primary_key_column = column.name
            
            if primary_key_column and editable_columns:
                # Convert id_value to an integer
                id_value = int(id_value)

                # Search for the row index corresponding to the primary key value
                row_idx = -1
                for row in range(table_widget.rowCount()):
                    item = table_widget.item(row, column_names.index(primary_key_column))
                    if item is not None and int(item.text()) == id_value:
                        row_idx = row
                        break

                if row_idx != -1:
                    item_values = [table_widget.item(row_idx, column_names.index(col)).text() for col in editable_columns]
                    dialog = QDialog(self)
                    dialog.setWindowTitle("Update Record")

                    # Increase the size of the dialog window
                    dialog.setGeometry(100, 100, 1024, 768)  # Adjust width and height as needed

                    layout = QGridLayout()  # Grid layout for two columns

                    # Add labels and line edits to the layout
                    for col, (col_name, value) in enumerate(zip(editable_columns, item_values)):
                        label = QLabel(col_name.replace("_", " ").title(), dialog)
                        line_edit = QLineEdit(dialog)
                        line_edit.setText(value)

                        # Calculate the row and column index for label and line edit
                        row = col // 2
                        col_offset = col % 2

                        # Add label and line edit to the grid layout
                        layout.addWidget(label, row, col_offset * 2)
                        layout.addWidget(line_edit, row, col_offset * 2 + 1)

                    submit_button = QPushButton("Submit", dialog)
                    layout.addWidget(submit_button, len(editable_columns) // 2 + 1, 0, 1, 2)  # Span button across both columns
                    
                    def update_record():
                        new_values = {}
                        for col, (col_name, value) in enumerate(zip(editable_columns, item_values)):
                            line_edit = layout.itemAtPosition(col // 2, (col % 2) * 2 + 1).widget()
                            new_values[col_name] = line_edit.text()

                        try:
                            updated_obj = dal.update(model_class, identifier={primary_key_column: id_value}, **new_values)
                            if updated_obj:
                                for col, value in new_values.items():
                                    table_widget.item(row_idx, column_names.index(col)).setText(value)
                                dialog.close()
                            else:
                                raise Exception("Failed to update the record")
                        except Exception as e:
                            self.showErrorDialog(f"An error occurred while updating the record: {e}")
                    
                    submit_button.clicked.connect(update_record)

                    dialog.setLayout(layout)
                    dialog.exec()
                else:
                    self.showErrorDialog(f"Row not found for {primary_key_column} value.")
            else:
                self.showErrorDialog("Primary key column or editable columns not found in the model class.")




    def deleteSelectedItems(self, table_widget, model_class_name, db_session, refreshTable=refreshTable, addUpdateButton=addUpdateButton):
        dal = DataAccessLayer(db_session)
        selected_rows = table_widget.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(table_widget, "No selection", "Please select the rows you want to delete.")
            return

        model_class = get_model_class(model_class_name)
        if model_class:
            table_obj = model_class.__table__
            primary_key_columns = [col.name for col in table_obj.primary_key]
            with engine.connect() as connection:
                for idx in sorted(selected_rows, reverse=True):
                    row_data = [table_widget.item(idx.row(), col).text() for col in range(table_widget.columnCount())]
                    identifier = {col: val for col, val in zip(primary_key_columns, row_data)}
                    try:
                        # Use the delete method from the data access layer
                        dal.delete(model_class, **identifier)
                        table_widget.removeRow(idx.row())
                    except IntegrityError as e:
                        QMessageBox.critical(table_widget, "Error", f"An error occurred while deleting the record: {e}")

                refreshTable(self, model_class_name, table_widget, addUpdateButton)



    def showErrorDialog(self, message):
        # Code to create and display an error dialog with the given message
        error_dialog = QMessageBox()
        error_dialog.setText(message)
        error_dialog.setIcon(QMessageBox.Icon.Critical)
        error_dialog.setWindowTitle("Error")
        error_dialog.exec()

    def clearLineEdits(self, columns, layout):
        """Clears the content of all QLineEdit widgets in the form."""
        for i in range(0, len(columns)):
            line_edit = layout.itemAt((i * 2) + 1).widget()
            if isinstance(line_edit, QLineEdit):
                line_edit.clear()

    
    
    def getFormData(self, columns, model_class, layout):
        data = {}
        for i in range(0, len(columns)):
            label = layout.itemAt(i * 2).widget()
            line_edit = layout.itemAt((i * 2) + 1).widget()  # Assuming line_edit is the correct widget type
            
            if isinstance(line_edit, QLineEdit):
                text_content = line_edit.text().strip()
                if text_content:
                    data[label.text()] = text_content
                else:
                    raise ValueError(f"Поле '{label.text()}' не может быть пустым.")
            else:
                # Handle other widget types like QComboBox, etc.
                pass
        
        return data

