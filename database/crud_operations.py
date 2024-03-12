from sqlalchemy import inspect
from sqlalchemy.exc import IntegrityError
from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem, QPushButton, QDialog, QLabel, QVBoxLayout, QLineEdit
from database.data_access_layer import DataAccessLayer
from database.database import engine, db_session
from database.get_model_class import get_model_class
class CrudOperations:
    def __init__(self, db_session):
        self.db_session = db_session
        self.dal = DataAccessLayer(db_session)

    def createItem(self, model_class_name, table_widget, layout):
        self.refreshTable = CrudOperations.refreshTable
        self.clearLineEdits = CrudOperations.clearLineEdits
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
                self.showErrorDialog("Значение уже существует в базе данных")
                db_session.rollback()
            else:
                self.refreshTable(self, model_class_name, table_widget)
                self.clearLineEdits(self, columns, layout)

    def refreshTable(self, model_class_name, table_widget):
        self.addUpdateButton = CrudOperations.addUpdateButton
        model_class = get_model_class(model_class_name)
        if model_class:
            table_widget.clear()
            with engine.connect() as connection:
                result = connection.execute(model_class.__table__.select())
                rows = result.fetchall()

            table_widget.setRowCount(len(rows))
            table_widget.setColumnCount(len(model_class.__table__.columns))

            # Mapping between database column names and display names
            display_names = {
                'ID_street': 'ID улицы',
                'street_name': 'Название улицы',
                'ID_type_construction': 'ID типа конструкции',
                'type_construction_name': 'Название типа конструкции',
                'ID_basic_project': 'ID базового проекта',
                'basic_project_name': 'Название базового проекта',
                'ID_appointment': 'ID назначения',
                'appointment_name': 'Название назначения',
                'ID_load_bearing_walls': 'ID несущих стен',
                'load_bearing_walls_name': 'Название несущих стен',
                'ID_building_roof': 'ID крыши',
                'building_roof_name': 'Название крыши',
                'ID_building_floor': 'ID пола',
                'building_floor_name': 'Название пола',
                'ID_facade': 'ID фасада',
                'facade_name': 'Название фасада',
                'ID_foundation': 'ID фундамента',
                'foundation_name': 'Название фундамента',
                'ID_management_company': 'ID управляющей компании',
                'management_company_name': 'Название управляющей компании',
                'ID_wear_rate': 'ID износа',
                'date': 'Дата',
                'wear_rate_name': 'Название степени',
                'ID_building': 'ID здания',
                # Add more mappings as needed
            }

            # Translate column names to display names
            header_labels = [display_names.get(col.name, col.name) for col in model_class.__table__.columns]
            table_widget.setHorizontalHeaderLabels(header_labels)

            for row_idx, row in enumerate(rows):
                for col_idx, col in enumerate(row):
                    item = QTableWidgetItem(str(col))
                    table_widget.setItem(row_idx, col_idx, item)
                self.addUpdateButton(self, row_idx, table_widget, model_class_name)




    def addUpdateButton(self, row_idx, table_widget, model_class_name):
        
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
                    self.refreshTable(self, model_class_name, get_model_class, table_widget, self.addUpdateButton)
            else:
                QMessageBox.warning(self, "No selection", "Please select a row to edit.")
                update_button = QPushButton("Update")
                update_button.clicked.connect(lambda: self.updateItem(row_idx))
                table_widget.setCellWidget(row_idx, table_widget.columnCount(), update_button)


    def handleUpdateButtonClick(self, model_class_name, table_widget):
        self.updateItem = CrudOperations.updateItem
        current_row = self.table_widget.currentRow()
        id_item = self.table_widget.item(current_row, 0)  # Assuming the first column is the ID
        if id_item is not None:
            self.updateItem(self, id_item.text(), model_class_name, table_widget)
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
                    layout = QVBoxLayout()
                    
                    input_fields = {}
                    for col, value in zip(editable_columns, item_values):
                        label = QLabel(col.replace("_", " ").title(), dialog)
                        input_field = QLineEdit(dialog)
                        input_field.setText(value)
                        layout.addWidget(label)
                        layout.addWidget(input_field)
                        input_fields[col] = input_field
                    
                    submit_button = QPushButton("Submit", dialog)
                    layout.addWidget(submit_button)
                    
                    for field_name, field_value in input_fields.items():
                        field_value.setPlaceholderText("Enter new value for " + field_name)
                    
                    def update_record():
                        new_values = {field_name: field_value.text() for field_name, field_value in input_fields.items()}
                        try:
                            updated_obj = dal.update(model_class, identifier={primary_key_column: id_value}, **new_values)
                            if updated_obj:
                                for col, value in zip(editable_columns, new_values.values()):
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



    def deleteSelectedItems(self, table_widget, model_class_name):
        dal = DataAccessLayer(db_session)
        self.refreshTable = CrudOperations.refreshTable
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

                self.refreshTable(self, model_class_name, table_widget)



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

