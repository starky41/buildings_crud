from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QTableWidget, QTableWidgetItem, QMessageBox, QHeaderView
from models import Street, TypeConstruction, BasicProject, Appointment, LoadBearingWalls, BuildingRoof, BuildingFloor, Facade, BuildingDescription, WearRate
from database import engine, db_session
from data_access_layer import DataAccessLayer
from sqlalchemy import inspect, and_
from sqlalchemy.exc import IntegrityError
from PyQt6.QtGui import QIcon

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

            save_button = QPushButton("Save")
            save_button.clicked.connect(self.createItem)
            self.layout.addWidget(save_button)
        
            # Create a QTableWidget to display the database table data
            self.table_widget = QTableWidget()
            self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
            self.layout.addWidget(self.table_widget)

            # Add a Refresh button to reload the data
            refresh_button = QPushButton("Refresh")
            refresh_button.clicked.connect(self.refreshTable)
            self.layout.addWidget(refresh_button)

            # Add a Delete button with an icon
            delete_button = QPushButton()
            delete_button.setIcon(QIcon("icons/trashbin.png"))  # Assuming there is an icon file at the specified path
            delete_button.clicked.connect(self.deleteSelectedItems)
            self.layout.addWidget(delete_button)

            self.setLayout(self.layout)
            self.refreshTable()

    def configureMainWindow(self):
        self.resize(640, 480)

    def deleteSelectedItems(self):
        dal = DataAccessLayer(db_session)
        selected_rows = self.table_widget.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "No selection", "Please select the rows you want to delete.")
            return

        model_class = get_model_class(self.model_class_name)
        if model_class:
            primary_key_columns = [col.name for col in model_class.__table__.primary_key]
            with engine.connect() as connection:
                for idx in sorted(selected_rows, reverse=True):
                    row_data = [self.table_widget.item(idx.row(), col).text() for col in range(self.table_widget.columnCount())]
                    identifier = {col: val for col, val in zip(primary_key_columns, row_data)}
                    try:
                        # Use the delete method from the data access layer
                        dal.delete(model_class, **identifier)
                        self.table_widget.removeRow(idx.row())
                    except IntegrityError as e:
                        QMessageBox.critical(self, "Error", f"An error occurred while deleting the record: {e}")

            self.refreshTable()



    def refreshTable(self):
        model_class = get_model_class(self.model_class_name)
        if model_class:
            # Clear existing data in the table widget
            self.table_widget.clear()

            # Fetch data from the database table
            with engine.connect() as connection:
                result = connection.execute(model_class.__table__.select())
                rows = result.fetchall()

            # Set the table dimensions based on the retrieved data
            self.table_widget.setRowCount(len(rows))
            self.table_widget.setColumnCount(len(model_class.__table__.columns))

            # Populate the table with the fetched data
            for row_idx, row in enumerate(rows):
                for col_idx, col in enumerate(row):
                    item = QTableWidgetItem(str(col))
                    self.table_widget.setItem(row_idx, col_idx, item)

            # Set table headers
            headers = [str(col) for col in model_class.__table__.columns.keys()]
            self.table_widget.setHorizontalHeaderLabels(headers)


    def showErrorDialog(self, message):
        # Code to create and display an error dialog with the given message
        error_dialog = QMessageBox()
        error_dialog.setText(message)
        error_dialog.setIcon(QMessageBox.Icon.Critical)
        error_dialog.setWindowTitle("Error")
        error_dialog.exec()

# ...

    def createItem(self):
        model_class = get_model_class(self.model_class_name)
        if model_class:
            # Use SQLAlchemy's inspect function to get the columns
            inspector = inspect(model_class)
            columns = [column.name for column in inspector.columns]
            try:
                data = self.getFormData(columns=columns, model_class=model_class)
                new_instance = model_class(**data)
                dal = DataAccessLayer(db_session)
                dal.create(new_instance)
            except ValueError as e:
                # When an exception occurs, open an error dialog showing the error message.
                self.showErrorDialog(str(e))
                db_session.rollback()
            except IntegrityError as e:
                # When an exception occurs, open an error dialog showing the error message.
                self.showErrorDialog(str("Вы не можете добавить значение, которое уже есть в базе данных"))
                db_session.rollback()
            else:
                # If no exceptions occurred, refresh the table and clear the line edits.
                self.refreshTable()
                self.clearLineEdits(columns)



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


from models import Street, TypeConstruction

def get_model_class(model_class_name):
    model_mapping = {
        'Street': Street,
        'TypeConstruction': TypeConstruction,
        'BasicProject': BasicProject,
        'Appointment': Appointment,
        'LoadBearingWalls': LoadBearingWalls,
        'BuildingRoof': BuildingRoof,
        'BuildingFloor': BuildingFloor,
        'Facade': Facade,
        'BuildingDescription': BuildingDescription,
        'WearRate': WearRate
        # Add more model mappings as needed
    }
    return model_mapping.get(model_class_name)