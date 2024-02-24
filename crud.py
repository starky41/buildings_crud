from PyQt6.QtWidgets import QWidget, QVBoxLayout, QDialog, QHBoxLayout, QInputDialog, QLineEdit, QPushButton, QLabel, QTableWidget, QTableWidgetItem, QMessageBox, QHeaderView
from models import Street, TypeConstruction, BasicProject, Appointment, LoadBearingWalls, BuildingRoof, BuildingFloor, Facade, BuildingDescription, WearRate
from database import engine, db_session
from data_access_layer import DataAccessLayer
from sqlalchemy.exc import IntegrityError
from PyQt6.QtGui import QIcon
from get_model_class import get_model_class
from crud_operations import CrudOperations

class CrudWindow(QWidget):
    def __init__(self, model_class_name):
        super().__init__()
        self.model_class_name = model_class_name
        self.initUI()

    def initUI(self):
        self.configureMainWindow()
        self.setWindowTitle(f"CRUD for {self.model_class_name}")
        self.layout = QVBoxLayout()

        model_class = get_model_class(self.model_class_name)
        if model_class:
            # Get the columns of the model table
            columns = model_class.__table__.columns
            primary_key_columns = [col.name for col in model_class.__table__.primary_key]
            for column in columns:
                if column.primary_key and column.autoincrement:
                    continue  # Skip creating LineEdits for autoincrement fields
                label = QLabel(column.name)
                line_edit = QLineEdit()
                self.layout.addWidget(label)
                self.layout.addWidget(line_edit)

            save_button = QPushButton("Создать")
            # Create an instance of CrudOperations
            self.crud_operations = CrudOperations()
            save_button.clicked.connect(lambda: self.crud_operations.createItem(self.model_class_name, db_session, get_model_class, self.getFormData, DataAccessLayer, CrudOperations.refreshTable, self.clearLineEdits, self.table_widget, CrudOperations.addUpdateButton))
            self.layout.addWidget(save_button)
        
            # Create a QTableWidget to display the database table data
            self.table_widget = QTableWidget()
            self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
            self.layout.addWidget(self.table_widget)

            # Add a Refresh button to reload the data
            refresh_button = QPushButton("Обновить")
            refresh_button.clicked.connect(lambda: CrudOperations.refreshTable(self, self.model_class_name, get_model_class, self.table_widget, CrudOperations.addUpdateButton))
            self.layout.addWidget(refresh_button)

            # Add a Delete button with an icon
            delete_button = QPushButton()
            delete_button.setIcon(QIcon("icons/trashbin.png"))
            delete_button.clicked.connect(lambda: CrudOperations.deleteSelectedItems(self, self.table_widget, self.model_class_name, db_session, get_model_class, CrudOperations.refreshTable))
            self.layout.addWidget(delete_button)

            update_button = QPushButton("Изменить")
            update_button.clicked.connect(lambda: self.handleUpdateButtonClick())
            self.layout.addWidget(update_button)

        
            self.setLayout(self.layout)
            self.crud_operations.refreshTable(self.model_class_name, get_model_class, self.table_widget, CrudOperations.addUpdateButton)

    def handleUpdateButtonClick(self):
            current_row = self.table_widget.currentRow()
            id_item = self.table_widget.item(current_row, 0)  # Assuming the first column is the ID
            if id_item is not None:
                self.updateItem(id_item.text())
            else:
                QMessageBox.warning(self, "Update Error", "Please select a valid row before updating.")
    def configureMainWindow(self):
        self.resize(640, 480)


    
    
    def updateItem(self, id_value):
        model_class = get_model_class(self.model_class_name)
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
                for row in range(self.table_widget.rowCount()):
                    item = self.table_widget.item(row, column_names.index(primary_key_column))
                    if item is not None and int(item.text()) == id_value:
                        row_idx = row
                        break

                if row_idx != -1:
                    item_values = [self.table_widget.item(row_idx, column_names.index(col)).text() for col in editable_columns]
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
                                    self.table_widget.item(row_idx, column_names.index(col)).setText(value)
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













    def clearLineEdits(self, columns):
        """Clears the content of all QLineEdit widgets in the form."""
        for i in range(0, len(columns)):
            line_edit = self.layout.itemAt((i * 2) + 1).widget()
            if isinstance(line_edit, QLineEdit):
                line_edit.clear()

    def getFormData(self, columns, model_class):
        data = {}
        for i in range(0, len(columns)):
            label = self.layout.itemAt(i * 2).widget()
            line_edit = self.layout.itemAt((i * 2) + 1).widget()  # Assuming line_edit is the correct widget type
            
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


